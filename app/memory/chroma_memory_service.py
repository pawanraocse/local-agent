import os
from chromadb import Client as ChromaClient
from chromadb.config import Settings
from langchain.memory import VectorStoreRetrieverMemory
from langchain_chroma import Chroma  # Updated import as per deprecation warning
from langchain_community.embeddings import OllamaEmbeddings

class ChromaMemoryService:
    """
    Service for managing agent memory using ChromaDB as a vector store.
    Provides add, retrieve, and search operations for agent context/history.
    """
    def __init__(self, persist_directory: str = "/app/documents/chroma_memory"):
        self.persist_directory = persist_directory
        os.makedirs(self.persist_directory, exist_ok=True)
        self.chroma_client = ChromaClient(Settings(persist_directory=self.persist_directory))
        self.collection_name = "agent_memory"
        ollama_host = os.getenv("OLLAMA_HOST", "http://ollama:11434")
        ollama_model = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:0.5b")
        self.vectorstore = Chroma(
            client=self.chroma_client,
            collection_name=self.collection_name,
            embedding_function=OllamaEmbeddings(base_url=ollama_host, model=ollama_model)
        )
        self.memory = VectorStoreRetrieverMemory(
            retriever=self.vectorstore.as_retriever(),
            memory_key="history",
            input_key="input"
        )

    def add_memory(self, input_text: str, metadata: dict = None):
        self.memory.save_context({"input": input_text}, metadata or {})

    def get_memory(self, query: str, k: int = 5):
        return self.memory.load_memory_variables({"input": query})

    def clear_memory(self):
        self.vectorstore.delete_collection(self.collection_name)
        ollama_host = os.getenv("OLLAMA_HOST", "http://ollama:11434")
        ollama_model = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:0.5b")
        self.vectorstore = Chroma(
            client=self.chroma_client,
            collection_name=self.collection_name,
            embedding_function=OllamaEmbeddings(base_url=ollama_host, model=ollama_model)
        )
        self.memory = VectorStoreRetrieverMemory(
            retriever=self.vectorstore.as_retriever(),
            memory_key="history",
            input_key="input"
        )
