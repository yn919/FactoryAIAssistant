import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, Mock
import sys
import os

# Add module path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from tests.fixtures.gemini_service import test_settings, mock_gemini_service

# Create test client
def create_test_client():
    """Create test client with injected mocks"""
    from app.core.dependencies import get_gemini_service
    
    def override_get_gemini_service():
        mock_service = Mock()
        mock_service.generate_response = AsyncMock(return_value="Test response message")
        mock_service.health_check = Mock(return_value=True)
        return mock_service
    
    app.dependency_overrides[get_gemini_service] = override_get_gemini_service
    client = TestClient(app)
    
    # Clean up overrides after test
    def cleanup():
        app.dependency_overrides.clear()
    
    return client, cleanup

def test_health_endpoint():
    """Test health check endpoint"""
    client, cleanup = create_test_client()
    try:
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    finally:
        cleanup()

def test_root_endpoint():
    """Test root endpoint"""
    client, cleanup = create_test_client()
    try:
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()
    finally:
        cleanup()

def test_chat_endpoint_success():
    """Test successful chat request"""
    client, cleanup = create_test_client()
    try:
        response = client.post(
            "/api/v1/chat",
            json={"message": "Hello"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert data["response"] == "Test response message"
    finally:
        cleanup()

def test_chat_endpoint_empty_message():
    """Test empty message error"""
    client, cleanup = create_test_client()
    try:
        response = client.post(
            "/api/v1/chat",
            json={"message": ""}
        )
        
        assert response.status_code == 422  # Validation error
    finally:
        cleanup()

def test_chat_endpoint_missing_message():
    """Test error when message field is missing"""
    client, cleanup = create_test_client()
    try:
        response = client.post(
            "/api/v1/chat",
            json={}
        )
        
        assert response.status_code == 422  # Validation error
    finally:
        cleanup()

def test_chat_endpoint_with_context():
    """Test chat request with context"""
    client, cleanup = create_test_client()
    try:
        response = client.post(
            "/api/v1/chat",
            json={
                "message": "Question",
                "context": "This is test context"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert data["response"] == "Test response message"
    finally:
        cleanup()

def test_chat_endpoint_service_error():
    """Test service error scenario"""
    from app.core.exceptions import GeminiAPIException
    from app.core.dependencies import get_gemini_service
    
    def override_get_gemini_service_error():
        mock_service = Mock()
        mock_service.generate_response = AsyncMock(side_effect=GeminiAPIException("API error"))
        mock_service.health_check = Mock(return_value=True)
        return mock_service
    
    app.dependency_overrides[get_gemini_service] = override_get_gemini_service_error
    client = TestClient(app)
    
    try:
        response = client.post(
            "/api/v1/chat",
            json={"message": "Hello"}
        )
        
        assert response.status_code == 503
    finally:
        app.dependency_overrides.clear()

def test_chat_endpoint_long_message():
    """Test validation for too long message"""
    client, cleanup = create_test_client()
    try:
        long_message = "a" * 1001  # Message over 1000 characters
        
        response = client.post(
            "/api/v1/chat",
            json={"message": long_message}
        )
        
        assert response.status_code == 422  # Validation error
    finally:
        cleanup()

def test_chat_endpoint_long_context():
    """Test validation for too long context"""
    client, cleanup = create_test_client()
    try:
        long_context = "a" * 501  # Context over 500 characters
        
        response = client.post(
            "/api/v1/chat",
            json={
                "message": "Test",
                "context": long_context
            }
        )
        
        assert response.status_code == 422  # Validation error
    finally:
        cleanup()

def test_health_endpoint_unhealthy():
    """Test health check endpoint when service is unhealthy"""
    from app.core.dependencies import get_gemini_service
    
    def override_get_gemini_service_unhealthy():
        mock_service = Mock()
        mock_service.generate_response = AsyncMock(return_value="Test response")
        mock_service.health_check = Mock(return_value=False)  # Service unhealthy
        return mock_service
    
    app.dependency_overrides[get_gemini_service] = override_get_gemini_service_unhealthy
    client = TestClient(app)
    
    try:
        response = client.get("/api/v1/health")
        assert response.status_code == 503
        assert "Gemini API is unavailable" in response.json()["detail"]
    finally:
        app.dependency_overrides.clear()

def test_health_endpoint_service_exception():
    """Test health check endpoint when service throws exception"""
    from app.core.dependencies import get_gemini_service
    from app.core.exceptions import GeminiAPIException
    
    def override_get_gemini_service_exception():
        mock_service = Mock()
        mock_service.health_check = Mock(side_effect=GeminiAPIException("Service error"))
        return mock_service
    
    app.dependency_overrides[get_gemini_service] = override_get_gemini_service_exception
    client = TestClient(app)
    
    try:
        response = client.get("/api/v1/health")
        assert response.status_code == 503
        assert "Service error" in response.json()["detail"]
    finally:
        app.dependency_overrides.clear()
