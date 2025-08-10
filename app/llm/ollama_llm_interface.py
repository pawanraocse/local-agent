import os
import logging
from langchain_community.llms import Ollama  # Updated import
from langchain_community.embeddings import OllamaEmbeddings

logger = logging.getLogger(__name__)

class OllamaLLMInterface:
    """
    Encapsulates the initialization and configuration of the local Ollama LLM interface.
    Promotes abstraction and testability for agentic workflows.
    """
    def __init__(self, model_name: str = None, temperature: float = 0.7):
        # Prefer model name from environment variable, fallback to argument, then default
        self.model_name = os.getenv("OLLAMA_MODEL") or model_name or "llama3"
        self.temperature = temperature
        logger.info(f"Initializing Ollama LLM with model: {self.model_name}")
        self.llm = self._init_llm()

    def _init_llm(self):
        """Initializes and returns the Ollama LLM instance."""
        ollama_host = os.getenv("OLLAMA_HOST", "http://ollama:11434")
        return Ollama(model=self.model_name, temperature=self.temperature, base_url=ollama_host)

    def get_llm(self):
        """Returns the underlying Ollama LLM instance for agent use."""
        return self.llm
