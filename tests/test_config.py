import os
import logging
import pytest
from app import config

def test_model_name_env(monkeypatch):
    monkeypatch.setenv("OLLAMA_MODEL", "test-model")
    # Reload config to pick up new env var
    import importlib
    importlib.reload(config)
    assert config.MODEL_NAME == "test-model"

def test_model_name_default(monkeypatch):
    monkeypatch.delenv("OLLAMA_MODEL", raising=False)
    import importlib
    importlib.reload(config)
    assert config.MODEL_NAME == "qwen2.5-coder:0.5b"

def test_chroma_collection_env(monkeypatch):
    monkeypatch.setenv("CHROMA_COLLECTION", "test_collection")
    import importlib
    importlib.reload(config)
    assert config.CHROMA_COLLECTION == "test_collection"

def test_chroma_collection_default(monkeypatch):
    monkeypatch.delenv("CHROMA_COLLECTION", raising=False)
    import importlib
    importlib.reload(config)
    assert config.CHROMA_COLLECTION == "agent_history"

