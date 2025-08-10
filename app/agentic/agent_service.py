from typing import List
import logging
import time
import re
from langchain_core.prompts import PromptTemplate
from langchain_core.language_models import BaseLanguageModel
from langchain_core.tools import BaseTool
from langchain.agents import AgentExecutor, create_react_agent
from dto.code_generation import CodeGenerationResponse

logger = logging.getLogger(__name__)

MAX_AGENT_ITERATIONS = 3
MAX_AGENT_EXECUTION_TIME = 15
CODE_BLOCK_REGEX = r"```(?:python)?\n(.*?)```"


class AgenticAIService:
    """
    A service for creating and running a ReAct agent with given tools and an Ollama LLM.
    Automatically optimizes for speed by skipping the ReAct loop when no tools are loaded.
    """

    def __init__(self, llm: BaseLanguageModel, tools: List[BaseTool], verbose: bool = False):
        self.llm = llm
        self.tools = tools or []
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

    def run(self, query: str) -> str:
        """
        Executes the agent against a user query, with timing logs.
        Uses a direct LLM call if no tools are loaded to avoid ReAct overhead.
        """
        try:
            logger.info(f"Running agent with query: {query}")
            start_time = time.time()

            # Fast-path: direct LLM call
            if not self.tools or not self.agent_executor:
                logger.info("No tools loaded — using direct LLM call for speed.")
                result = self.llm.invoke(query)
                elapsed = time.time() - start_time
                logger.info(f"Direct LLM call completed in {elapsed:.2f} seconds.")
                text = result if isinstance(result, str) else str(result)
                code = self._extract_code(text)
                return code

            # Standard ReAct agent execution
            result = self.agent_executor.invoke({"input": query})
            elapsed = time.time() - start_time
            logger.info(f"Agent execution completed in {elapsed:.2f} seconds.")

            # Handle multiple possible keys for final output
            output = (
                    result.get("code")
                    or result.get("output")
                    or result.get("output_text")
                    or str(result)
            )
            code = self._extract_code(output)
            return code

        except Exception as e:
            logger.error(f"Agent execution failed: {e}", exc_info=True)
            return "error"
