import pytest
from unittest.mock import patch, MagicMock
from app.agent import Agent

def test_agent_instantiation():
    agent = Agent()
    assert agent.llm is not None
    assert agent.collection is not None

@patch("app.agent.Ollama")
@patch("app.agent.chromadb.Client")
def test_generate_code(mock_chroma_client, mock_ollama):
    mock_llm = MagicMock()
    mock_chain = MagicMock()
    mock_chain.run.return_value = "def foo(): pass"
    mock_ollama.return_value = mock_llm
    mock_chroma = MagicMock()
    mock_chroma.get_or_create_collection.return_value = MagicMock()
    mock_chroma_client.return_value = mock_chroma
    with patch("app.agent.LLMChain", return_value=mock_chain):
        agent = Agent()
        result = agent.generate_code("Write a Python function")
        assert "def foo" in result

@patch("app.agent.Ollama")
@patch("app.agent.chromadb.Client")
def test_review_code(mock_chroma_client, mock_ollama):
    mock_llm = MagicMock()
    mock_chain = MagicMock()
    mock_chain.run.return_value = "Looks good, but add error handling."
    mock_ollama.return_value = mock_llm
    mock_chroma = MagicMock()
    mock_chroma.get_or_create_collection.return_value = MagicMock()
    mock_chroma_client.return_value = mock_chroma
    with patch("app.agent.LLMChain", return_value=mock_chain):
        agent = Agent()
        result = agent.review_code("def foo(): pass")
        assert "error handling" in result

@patch("app.agent.chromadb.Client")
def test_get_history(mock_chroma_client):
    mock_chroma = MagicMock()
    mock_chroma.get_or_create_collection.return_value.get.return_value = {
        "documents": ["doc1", "doc2"],
        "metadatas": [{}, {}],
        "ids": ["1", "2"]
    }
    mock_chroma_client.return_value = mock_chroma
    agent = Agent()
    history = agent.get_history(limit=2)
    assert len(history["documents"]) == 2

@patch("app.agent.Ollama")
@patch("app.agent.chromadb.Client")
def test_generate_code_empty_task(mock_chroma_client, mock_ollama):
    mock_llm = MagicMock()
    mock_chain = MagicMock()
    mock_chain.run.return_value = ""
    mock_ollama.return_value = mock_llm
    mock_chroma = MagicMock()
    mock_chroma.get_or_create_collection.return_value = MagicMock()
    mock_chroma_client.return_value = mock_chroma
    with patch("app.agent.LLMChain", return_value=mock_chain):
        agent = Agent()
        result = agent.generate_code("")
        assert result == ""

@patch("app.agent.Ollama")
@patch("app.agent.chromadb.Client")
def test_generate_code_markdown_strip(mock_chroma_client, mock_ollama):
    mock_llm = MagicMock()
    mock_chain = MagicMock()
    mock_chain.run.return_value = "```python\ndef foo(): pass\n```"
    mock_ollama.return_value = mock_llm
    mock_chroma = MagicMock()
    mock_chroma.get_or_create_collection.return_value = MagicMock()
    mock_chroma_client.return_value = mock_chroma
    with patch("app.agent.LLMChain", return_value=mock_chain):
        agent = Agent()
        result = agent.generate_code("Write a Python function")
        assert result.strip() == "def foo(): pass"

@patch("app.agent.Ollama")
@patch("app.agent.chromadb.Client")
def test_generate_code_llm_failure(mock_chroma_client, mock_ollama):
    mock_llm = MagicMock()
    mock_chain = MagicMock()
    mock_chain.run.side_effect = Exception("LLM error")
    mock_ollama.return_value = mock_llm
    mock_chroma = MagicMock()
    mock_chroma.get_or_create_collection.return_value = MagicMock()
    mock_chroma_client.return_value = mock_chroma
    with patch("app.agent.LLMChain", return_value=mock_chain):
        agent = Agent()
        with pytest.raises(Exception):
            agent.generate_code("Write a Python function")

@patch("app.agent.Ollama")
@patch("app.agent.chromadb.Client")
def test_get_history_chromadb_failure(mock_chroma_client, mock_ollama):
    mock_llm = MagicMock()
    mock_ollama.return_value = mock_llm
    mock_chroma = MagicMock()
    mock_chroma.get_or_create_collection.return_value.get.side_effect = Exception("ChromaDB error")
    mock_chroma_client.return_value = mock_chroma
    agent = Agent()
    with pytest.raises(Exception):
        agent.get_history(limit=2)
