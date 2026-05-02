"""依存性注入のテスト"""
import pytest
from unittest.mock import Mock, patch
from app.core.dependencies import get_gemini_service
from app.core.config import Settings
from app.services.gemini_service import GeminiService


def test_get_gemini_service_success():
    """Geminiサービス依存性注入成功テスト"""
    mock_settings = Settings(
        gemini_api_key="test_key",
        gemini_model="gemini-1.5-pro"
    )
    
    with patch('app.core.dependencies.GeminiService') as mock_gemini_class:
        mock_service = Mock()
        mock_gemini_class.return_value = mock_service
        
        result = get_gemini_service(mock_settings)
        
        assert result == mock_service
        mock_gemini_class.assert_called_once_with(mock_settings)


def test_get_gemini_service_no_api_key():
    """APIキーなしでのGeminiサービス依存性注入失敗テスト"""
    mock_settings = Settings(gemini_api_key=None)
    
    with patch('app.core.dependencies.GeminiService') as mock_gemini_class:
        mock_gemini_class.side_effect = ValueError("GEMINI_API_KEY is not configured")
        
        with pytest.raises(ValueError, match="GEMINI_API_KEY is not configured"):
            get_gemini_service(mock_settings)
