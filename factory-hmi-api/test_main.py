import pytest
from fastapi.testclient import TestClient
from main import app

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
    assert data["status"] == "normal" or data["status"] == "warning"
    assert isinstance(data["temperature"], float)
    assert isinstance(data["pressure"], float)
    assert isinstance(data["vibration"], float)

def test_ask_ai_normal_case():
    response = client.post("/ask", json={"message": "こんにちは"})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert isinstance(data["answer"], str)
    assert len(data["answer"]) > 0

def test_ask_ai_empty_message():
    response = client.post("/ask", json={"message": ""})
    assert response.status_code == 200  # FastAPI's default for empty string is 200 if valid pydantic
    data = response.json()
    assert "answer" in data
    assert isinstance(data["answer"], str)

def test_ask_ai_long_message():
    long_message = "これは非常に長いメッセージです。" * 100
    response = client.post("/ask", json={"message": long_message})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert isinstance(data["answer"], str)
