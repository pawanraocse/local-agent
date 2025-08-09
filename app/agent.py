"""
Agent module for orchestrating LLM (Ollama), LangChain, and vector DB (ChromaDB) for coding tasks.
Follows clean architecture: modular, testable, extensible.
"""
from langchain.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import chromadb
import logging
from typing import List, Dict
from config import MODEL_NAME, CHROMA_COLLECTION, OLLAMA_HOST
import re

# Constants
# MODEL_NAME and CHROMA_COLLECTION are now imported from config.py for environment-driven configuration

# Structured logging setup
logger = logging.getLogger("agent")
logger.setLevel(logging.INFO)

class Agent:
    def __init__(self):
        # Initialize Ollama LLM
        self.llm = Ollama(model=MODEL_NAME, base_url=OLLAMA_HOST)
        # Initialize ChromaDB for history/RAG
        self.chroma_client = chromadb.Client()
        self.collection = self.chroma_client.get_or_create_collection(CHROMA_COLLECTION)

    def _strip_code_fences(self, text: str) -> str:
        """
        Remove markdown code fences, language identifiers, and leading/trailing whitespace from LLM output.
        """
        # Remove all triple backtick code blocks (with or without language identifier)
        text = re.sub(r"```[a-zA-Z0-9]*\\n", "", text)  # Remove opening ```python\n or similar
        text = re.sub(r"```", "", text)  # Remove any remaining closing ```
        # Remove any language identifier left on its own line (e.g., 'python' at the start, even with leading whitespace)
        text = re.sub(r"^\s*([a-zA-Z0-9]+)\s*\n", "", text)
        # Remove any remaining single backticks
        text = re.sub(r"`([^`]*)`", r"\1", text)
        return text.strip()

    def generate_code(self, task: str, context: str = "") -> str:
        """
        Generate code for a given task using LLM and LangChain.
        Persists the request and response in vector DB for RAG.
        """
        prompt = PromptTemplate.from_template(
            """You are a senior software developer. Task: {task}\nContext: {context}\nGenerate production-ready code."""
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        response = chain.run({"task": task, "context": context})
        # Persist to vector DB
        self.collection.add(
            documents=[response],
            metadatas=[{"task": task, "context": context}],
            ids=[str(hash(task + context))]
        )
        logger.info(f"Code generated for task: {task}")
        # Post-process to remove markdown/code fences
        return self._strip_code_fences(response)

    def review_code(self, code: str) -> str:
        """
        Review code for quality, bugs, and improvements.
        Persists the review in vector DB.
        """
        prompt = PromptTemplate.from_template(
            """You are a senior software developer. Review the following code for quality, bugs, and improvements:\n{code}"""
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        response = chain.run({"code": code})
        self.collection.add(
            documents=[response],
            metadatas=[{"reviewed_code": code}],
            ids=[str(hash(code))]
        )
        logger.info("Code review completed.")
        # Post-process to remove markdown/code fences
        return self._strip_code_fences(response)

    def get_history(self, limit: int = 10) -> List[Dict]:
        """
        Retrieve recent agent history from vector DB.
        """
        results = self.collection.get(limit=limit)
        logger.info(f"Fetched {len(results['documents'])} history items.")
        return results
