"""Test helper functions"""
from unittest.mock import Mock, AsyncMock
from fastapi import Request
from fastapi.responses import JSONResponse


def create_mock_request(method: str = "GET", path: str = "/") -> Mock:
    """Create mock of FastAPI request"""
    mock_request = Mock(spec=Request)
    mock_request.method = method
    mock_request.url = Mock()
    mock_request.url.path = path
    return mock_request


def create_mock_json_response(status_code: int = 200, content: dict = None) -> Mock:
    """Create mock of JSON response"""
    mock_response = Mock(spec=JSONResponse)
    mock_response.status_code = status_code
    mock_response.body = str(content or {}).encode()
    return mock_response


def assert_json_response_contains(response: JSONResponse, expected_content: str, expected_status: int = None):
    """Helper function to verify JSON response content"""
    if expected_status:
        assert response.status_code == expected_status
    
    content = response.body.decode()
    assert expected_content in content


def create_mock_exception(message: str, status_code: int = 500, details: dict = None):
    """Create mock of exception"""
    from app.core.exceptions import FactoryAIException
    return FactoryAIException(
        message=message,
        status_code=status_code,
        details=details or {}
    )


def create_mock_gemini_service(response_text: str = "Test response", health_check_result: bool = True):
    """Create mock of Gemini service"""
    from app.services.gemini_service import GeminiService
    
    mock_service = Mock(spec=GeminiService)
    mock_service.generate_response = AsyncMock(return_value=response_text)
    mock_service.health_check = Mock(return_value=health_check_result)
    return mock_service


def create_mock_gemini_model(response_text: str = "Test response", side_effect: Exception = None):
    """Create mock of Gemini model"""
    mock_model = Mock()
    mock_response = Mock()
    mock_response.text = response_text
    
    if side_effect:
        mock_model.generate_content.side_effect = side_effect
    else:
        mock_model.generate_content.return_value = mock_response
    
    return mock_model
