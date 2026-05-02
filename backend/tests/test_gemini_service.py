"""Geminiサービスのテスト"""
import pytest
from unittest.mock import Mock, patch
from app.services.gemini_service import GeminiService
from app.core.exceptions import GeminiAPIException
from tests.data.test_messages import GEMINI_TEST_MESSAGES


def test_gemini_service_init_success(mock_settings):
    """Geminiサービスの初期化成功テスト"""
    with patch('app.services.gemini_service.genai') as mock_genai:
        mock_model = mock_genai.GenerativeModel.return_value
        
        service = GeminiService(mock_settings)
        
        assert service.settings == mock_settings
        mock_genai.configure.assert_called_once_with(api_key=mock_settings.gemini_api_key)
        mock_genai.GenerativeModel.assert_called_once_with("gemini-1.5-pro")
        assert service.model == mock_model


def test_gemini_service_init_no_api_key():
    """APIキーがない場合の初期化失敗テスト"""
    from app.core.config import Settings
    settings = Settings(gemini_api_key=None)
    
    with pytest.raises(ValueError, match="GEMINI_API_KEY is not configured"):
        GeminiService(settings)


@pytest.mark.asyncio
async def test_generate_response_success(mock_settings, mock_model):
    """応答生成成功テスト"""
    with patch('app.services.gemini_service.genai') as mock_genai:
        mock_genai.GenerativeModel.return_value = mock_model
        
        service = GeminiService(mock_settings)
        result = await service.generate_response(GEMINI_TEST_MESSAGES["simple"])
        
        mock_response = mock_model.generate_content.return_value
        assert result == mock_response.text
        mock_model.generate_content.assert_called_once_with(GEMINI_TEST_MESSAGES["simple"])


@pytest.mark.asyncio
async def test_generate_response_with_context(mock_settings, mock_model):
    """コンテキスト付き応答生成テスト"""
    with patch('app.services.gemini_service.genai') as mock_genai:
        mock_genai.GenerativeModel.return_value = mock_model
        
        service = GeminiService(mock_settings)
        result = await service.generate_response(
            GEMINI_TEST_MESSAGES["with_context"], 
            GEMINI_TEST_MESSAGES["context"]
        )
        
        mock_response = mock_model.generate_content.return_value
        assert result == mock_response.text
        mock_model.generate_content.assert_called_once_with(GEMINI_TEST_MESSAGES["expected_prompt"])


@pytest.mark.asyncio
async def test_generate_response_empty_response(mock_settings):
    """空レスポンスのテスト"""
    with patch('app.services.gemini_service.genai') as mock_genai:
        mock_model = mock_genai.GenerativeModel.return_value
        mock_response = mock_model.generate_content.return_value
        mock_response.text = GEMINI_TEST_MESSAGES["empty_response"]
        
        service = GeminiService(mock_settings)
        result = await service.generate_response(GEMINI_TEST_MESSAGES["simple"])
        
        assert result == "申し訳ありません。応答を生成できませんでした。"


@pytest.mark.asyncio
async def test_generate_response_api_error(mock_settings):
    """APIエラーのテスト"""
    with patch('app.services.gemini_service.genai') as mock_genai:
        mock_model = mock_genai.GenerativeModel.return_value
        mock_model.generate_content.side_effect = Exception("API Error")
        
        service = GeminiService(mock_settings)
        
        with pytest.raises(GeminiAPIException, match="Gemini API呼び出しに失敗しました"):
            await service.generate_response(GEMINI_TEST_MESSAGES["simple"])


def test_health_check_success(mock_settings):
    """ヘルスチェック成功テスト"""
    with patch('app.services.gemini_service.genai') as mock_genai:
        mock_model = mock_genai.GenerativeModel.return_value
        mock_model.generate_content.return_value = Mock()
        
        service = GeminiService(mock_settings)
        result = service.health_check()
        
        assert result is True
        mock_model.generate_content.assert_called_once_with(GEMINI_TEST_MESSAGES["health_check"])


def test_health_check_failure(mock_settings):
    """ヘルスチェック失敗テスト"""
    with patch('app.services.gemini_service.genai') as mock_genai:
        mock_model = mock_genai.GenerativeModel.return_value
        mock_model.generate_content.side_effect = Exception("Health check failed")
        
        service = GeminiService(mock_settings)
        result = service.health_check()
        
        assert result is False
