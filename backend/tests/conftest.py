import pytest
import sys
import os
from unittest.mock import Mock, AsyncMock, patch
from app.core.config import Settings

# Add module path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


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
def mock_settings():
    """Test settings (simplified)"""
    from tests.data.test_messages import CONFIG_TEST_DATA
    return Settings(
        gemini_api_key=CONFIG_TEST_DATA["mock_api_key"],
        gemini_model="gemini-1.5-pro"
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


@pytest.fixture
def mock_model():
    """Mock of Gemini model"""
    mock_model = Mock()
    mock_response = Mock()
    mock_response.text = "Test response"
    mock_model.generate_content.return_value = mock_response
    return mock_model


@pytest.fixture(autouse=True)
def mock_settings_global(test_settings):
    """Mock settings (auto-applied)"""
    with patch('app.core.config.Settings.Config.env_file', None):
        with patch.dict('os.environ', {}, clear=True):
            with patch('app.core.config.get_settings', return_value=test_settings):
                yield


@pytest.fixture
def mock_request():
    """Mock of FastAPI request"""
    from fastapi import Request
    return Mock(spec=Request)
