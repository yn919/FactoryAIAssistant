import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from main import app, get_model

class MockResponse:
    text = "mocked answer"

def mock_model():
    mock = MagicMock()
    mock.generate_content.return_value = MockResponse()
    return mock

app.dependency_overrides[get_model] = mock_model

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Factory HMI API"}

def test_sensor_normal_status():
    response = client.get("/sensor")
    assert response.status_code == 200
    data = response.json()
    assert "temperature" in data
    assert "pressure" in data
    assert "vibration" in data
    assert "status" in data
    assert data["status"] in ["normal", "warning"]
    assert isinstance(data["temperature"], float)
    assert isinstance(data["pressure"], float)
    assert isinstance(data["vibration"], float)

def test_ask_ai_normal_case():
    response = client.post("/ask", json={"message": "こんにちは"})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert data["answer"] == "mocked answer"

def test_ask_ai_empty_message():
    response = client.post("/ask", json={"message": ""})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert data["answer"] == "mocked answer"

def test_ask_ai_long_message():
    long_message = "これは非常に長いメッセージです。" * 100
    response = client.post("/ask", json={"message": long_message})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert data["answer"] == "mocked answer"
