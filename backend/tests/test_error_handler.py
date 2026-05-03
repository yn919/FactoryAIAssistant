"""Tests for error handlers"""
import pytest
from unittest.mock import patch
from fastapi.responses import JSONResponse
from app.core.exceptions import FactoryAIException, GeminiAPIException
from app.middleware.error_handler import factory_ai_exception_handler, general_exception_handler
from tests.data.test_messages import EXCEPTION_TEST_MESSAGES
from tests.utils.test_helpers import assert_json_response_contains


@pytest.mark.asyncio
async def test_factory_ai_exception_handler(mock_request):
    """Test FactoryAIException handler"""
    mock_exception = FactoryAIException(
        message=EXCEPTION_TEST_MESSAGES["factory_ai"],
        status_code=400,
        details={"field": "value"}
    )
    
    with patch('app.middleware.error_handler.logger') as mock_logger:
        response = await factory_ai_exception_handler(mock_request, mock_exception)
        
        assert isinstance(response, JSONResponse)
        assert response.status_code == 400
        
        assert_json_response_contains(response, EXCEPTION_TEST_MESSAGES["factory_ai"], 400)
        
        mock_logger.error.assert_called_once()


@pytest.mark.asyncio
async def test_factory_ai_exception_handler_no_details(mock_request):
    """Test FactoryAIException handler without details"""
    mock_exception = FactoryAIException("Simple error")
    
    with patch('app.middleware.error_handler.logger') as mock_logger:
        response = await factory_ai_exception_handler(mock_request, mock_exception)
        
        assert response.status_code == 500
        mock_logger.error.assert_called_once()


@pytest.mark.asyncio
async def test_general_exception_handler(mock_request):
    """Test general exception handler"""
    mock_exception = Exception(EXCEPTION_TEST_MESSAGES["unexpected"])
    
    with patch('app.middleware.error_handler.logger') as mock_logger:
        response = await general_exception_handler(mock_request, mock_exception)
        
        assert isinstance(response, JSONResponse)
        assert response.status_code == 500
        
        assert_json_response_contains(response, EXCEPTION_TEST_MESSAGES["internal_server"], 500)
        
        mock_logger.error.assert_called_once_with(
            f"Unhandled exception: {EXCEPTION_TEST_MESSAGES['unexpected']}",
            exc_info=True
        )


@pytest.mark.asyncio
async def test_general_exception_handler_gemini_api(mock_request):
    """Test general handler for GeminiAPIException"""
    mock_exception = GeminiAPIException(EXCEPTION_TEST_MESSAGES["gemini_api"])
    
    with patch('app.middleware.error_handler.logger') as mock_logger:
        response = await general_exception_handler(mock_request, mock_exception)
        
        assert response.status_code == 500
        mock_logger.error.assert_called_once()
