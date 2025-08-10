from typing import List
import logging
import time
import re
from langchain_core.prompts import PromptTemplate
from langchain_core.language_models import BaseLanguageModel
from langchain_core.tools import BaseTool
from langchain.agents import AgentExecutor, create_react_agent
from dto.code_generation import CodeGenerationResponse
from memory.chroma_memory_service import ChromaMemoryService

logger = logging.getLogger(__name__)

MAX_AGENT_ITERATIONS = 8  # Increased from 3 to 8 for deeper tool use
MAX_AGENT_EXECUTION_TIME = 60  # Increased from 15 to 60 seconds for longer tasks
CODE_BLOCK_REGEX = r"```(?:python)?\n(.*?)```"


class AgenticAIService:
    """
    A service for creating and running a ReAct agent with given tools and an Ollama LLM.
    Automatically optimizes for speed by skipping the ReAct loop when no tools are loaded.
    """

    def __init__(self, llm: BaseLanguageModel, tools: List[BaseTool], memory_service: ChromaMemoryService = None, verbose: bool = False):
        self.llm = llm
        self.tools = tools or []
        self.memory_service = memory_service
        self.verbose = verbose

        logger.info(f"Initializing agent with {len(self.tools)} tools.")
        self.prompt = self._build_prompt()

        # Only create the agent executor if there are tools
        self.agent_executor = self._create_agent_executor() if self.tools else None

    def _build_prompt(self) -> PromptTemplate:
        """
        Builds a robust prompt for the ReAct agent.
        Matches LangChain's expected variables: {tools}, {tool_names}.
        """
        tools_str = "\n".join([f"- {tool.name}: {tool.description}" for tool in self.tools])
        tool_names_str = ", ".join([tool.name for tool in self.tools])

        prompt_template = """
You are an advanced AI assistant that uses the ReAct reasoning framework.

You have access to the following tools:
{tools}

Tool Names: {tool_names}

Follow this format exactly:

Question: the input question you must answer
Thought: your reasoning about what to do next
Action: the tool name to use (must be one of [{tool_names}])
Action Input: the input for that tool
Observation: the result from the tool
... (repeat Thought/Action/Action Input/Observation as needed)
Final Answer: the final answer to the original question

Begin!

Question: {input}
{agent_scratchpad}
"""
        return PromptTemplate(
            template=prompt_template.strip(),
            input_variables=["input", "agent_scratchpad", "tools", "tool_names"],
            partial_variables={"tools": tools_str, "tool_names": tool_names_str}
        )

    def _create_agent_executor(self) -> AgentExecutor:
        """
        Creates a ReAct agent executor using the provided LLM, tools, and prompt.
        """
        agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )

        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=self.verbose,
            handle_parsing_errors=True,
            max_iterations=MAX_AGENT_ITERATIONS,  # Keep iterations small for speed
            max_execution_time=MAX_AGENT_EXECUTION_TIME  # Limit runtime to avoid long stalls
        )

    def _extract_code(self, text: str) -> str:
        """
        Extracts the first Python code block from markdown text,
        or returns the full text if no code block is found.
        """
        matches = re.findall(CODE_BLOCK_REGEX, text, re.DOTALL)
        if matches:
            return matches[0].strip()
        return text.strip()

    def run(self, query: str) -> dict:
        """
        Executes the agent against a user query, with timing logs and step-by-step trace logging.
        Uses a direct LLM call if no tools are loaded to avoid ReAct overhead.
        Persists each query/response in vector memory for context-aware, auditable flows.
        Logs each agent step (Thought, Action, Observation) for traceability.
        Returns a structured error DTO if the agent stops due to limits, including the full reasoning trace.
        """
        try:
            logger.info(f"Running agent with query: {query}")
            start_time = time.time()
            context = None
            step_trace = []
            # Retrieve relevant memory context for the query (RAG)
            if self.memory_service:
                logger.info("Retrieving memory context for query...")
                context = self.memory_service.get_memory(query)
                logger.info(f"Memory context: {context}")

            # Fast-path: direct LLM call
            if not self.tools or not self.agent_executor:
                logger.info("No tools loaded — using direct LLM call for speed.")
                result = self.llm.invoke(query)
                elapsed = time.time() - start_time
                logger.info(f"Direct LLM call completed in {elapsed:.2f} seconds.")
                text = result if isinstance(result, str) else str(result)
                code = self._extract_code(text)
                if self.memory_service:
                    self.memory_service.add_memory(query, {"output": code, "context": context})
                return {"code": code, "trace": step_trace, "model": getattr(self.llm, 'model_name', 'unknown')}

            # Standard ReAct agent execution with step-by-step logging
            agent_input = {"input": query}
            if context and isinstance(context, dict) and context.get("history"):
                agent_input["history"] = context["history"]
            try:
                for step in self.agent_executor.stream(agent_input):
                    if "intermediate_steps" in step:
                        for s in step["intermediate_steps"]:
                            action = getattr(s[0], "tool", None)
                            action_input = getattr(s[0], "tool_input", None)
                            observation = s[1]
                            logger.info(f"[Agent Step] Action: {action}, Input: {action_input}, Observation: {observation}")
                            step_trace.append({"action": action, "input": action_input, "observation": observation})
                    if "output" in step:
                        logger.info(f"[Agent Output] {step['output']}")
                        output = step["output"]
                        code = self._extract_code(output)
                        if self.memory_service:
                            self.memory_service.add_memory(query, {"output": code, "context": context, "trace": step_trace})
                        return {"code": code, "trace": step_trace, "model": getattr(self.llm, 'model_name', 'unknown')}
                # If we exit the loop without returning, agent likely hit a limit
                logger.warning("Agent stopped due to iteration or time limit. Returning partial trace.")
                return {
                    "error": "Agent stopped due to iteration or time limit.",
                    "trace": step_trace,
                    "model": getattr(self.llm, 'model_name', 'unknown')
                }
            except Exception as agent_exc:
                logger.error(f"Agent execution failed: {agent_exc}", exc_info=True)
                return {
                    "error": str(agent_exc),
                    "trace": step_trace,
                    "model": getattr(self.llm, 'model_name', 'unknown')
                }
        except Exception as e:
            logger.error(f"Agent execution failed: {e}", exc_info=True)
            return {"error": str(e), "trace": [], "model": getattr(self.llm, 'model_name', 'unknown')}
