"""エラーハンドラーのテスト"""
import pytest
from unittest.mock import Mock, patch
from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.exceptions import FactoryAIException, GeminiAPIException
from app.middleware.error_handler import factory_ai_exception_handler, general_exception_handler


@pytest.mark.asyncio
async def test_factory_ai_exception_handler():
    """FactoryAIExceptionハンドラーテスト"""
    mock_request = Mock(spec=Request)
    mock_exception = FactoryAIException(
        message="Test error",
        status_code=400,
        details={"field": "value"}
    )
    
    with patch('app.middleware.error_handler.logger') as mock_logger:
        response = await factory_ai_exception_handler(mock_request, mock_exception)
        
        assert isinstance(response, JSONResponse)
        assert response.status_code == 400
        
        content = response.body.decode()
        assert "Test error" in content
        assert "400" in content
        
        mock_logger.error.assert_called_once()


@pytest.mark.asyncio
async def test_factory_ai_exception_handler_no_details():
    """詳細なしFactoryAIExceptionハンドラーテスト"""
    mock_request = Mock(spec=Request)
    mock_exception = FactoryAIException("Simple error")
    
    with patch('app.middleware.error_handler.logger') as mock_logger:
        response = await factory_ai_exception_handler(mock_request, mock_exception)
        
        assert response.status_code == 500
        mock_logger.error.assert_called_once()


@pytest.mark.asyncio
async def test_general_exception_handler():
    """一般例外ハンドラーテスト"""
    mock_request = Mock(spec=Request)
    mock_exception = Exception("Unexpected error")
    
    with patch('app.middleware.error_handler.logger') as mock_logger:
        response = await general_exception_handler(mock_request, mock_exception)
        
        assert isinstance(response, JSONResponse)
        assert response.status_code == 500
        
        content = response.body.decode()
        assert "内部サーバーエラーが発生しました" in content
        assert "500" in content
        
        mock_logger.error.assert_called_once_with(
            "Unhandled exception: Unexpected error",
            exc_info=True
        )


@pytest.mark.asyncio
async def test_general_exception_handler_gemini_api():
    """GeminiAPIExceptionの一般ハンドラーテスト"""
    mock_request = Mock(spec=Request)
    mock_exception = GeminiAPIException("API Error")
    
    with patch('app.middleware.error_handler.logger') as mock_logger:
        response = await general_exception_handler(mock_request, mock_exception)
        
        assert response.status_code == 500
        mock_logger.error.assert_called_once()
