import pytest

def test_generate_code_real_model():
    from app.main import app
    from fastapi.testclient import TestClient
    client = TestClient(app)
    response = client.post("/generate", json={"task": "Write a Python function to add two numbers", "context": ""})
    assert response.status_code == 200
    data = response.json()
    assert "code" in data
    assert "def" in data["code"]
