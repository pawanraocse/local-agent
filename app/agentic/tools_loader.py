from langchain_community.agent_toolkits.load_tools import load_tools
import logging
from typing import List, Any

logger = logging.getLogger(__name__)

def load_agent_tools(llm: Any, tool_names: List[str] = None):
    """
    Loads and returns a list of agent tools for the given LLM.
    :param llm: The LLM instance to use with the tools.
    :param tool_names: List of tool names to load. Defaults to available tools only.
    :return: List of loaded tools.
    """
    if tool_names is None:
        tool_names = [
            # "wikipedia",
            # "llm-math",
            # "serpapi",  # Uncomment if you have an API key
            # "arxiv",    # Uncomment if you want arXiv search
            # "terminal", # Uncomment if you want shell access
        ]
    logger.info(f"Loading agent tools: {tool_names}")
    return load_tools(tool_names, llm=llm)
