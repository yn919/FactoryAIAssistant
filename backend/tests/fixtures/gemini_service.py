import pytest
from unittest.mock import Mock, AsyncMock, patch
from app.core.config import Settings


@pytest.fixture
def test_settings():
    """Test settings"""
    return Settings(
        gemini_api_key="mock_test_api_key_12345",
        server_host="localhost",
        server_port=8000,
        cors_origins=["http://localhost:3000"],
        log_level="INFO",
        app_name="Test Factory AI Assistant API",
        app_version="1.0.0-test",
        gemini_model="gemini-1.5-pro",
        environment="test"
    )


@pytest.fixture
def mock_gemini_service():
    """Complete mock of Gemini service"""
    from app.services.gemini_service import GeminiService
    
    mock_service = Mock(spec=GeminiService)
    mock_service.generate_response = AsyncMock(return_value="Test response message")
    mock_service.health_check = Mock(return_value=True)
    
    return mock_service


@pytest.fixture
def mock_gemini_response():
    """Mock response from Gemini API"""
    mock_response = Mock()
    mock_response.text = "This is test response"
    return mock_response


@pytest.fixture(autouse=True)
def mock_settings(test_settings):
    """Mock settings"""
    with patch('app.core.config.get_settings', return_value=test_settings):
        yield
