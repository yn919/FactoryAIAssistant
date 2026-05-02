"""Geminiサービスのテスト"""
import pytest
from unittest.mock import Mock, AsyncMock, patch
from app.services.gemini_service import GeminiService
from app.core.config import Settings
from app.core.exceptions import GeminiAPIException


@pytest.fixture
def mock_settings():
    """テスト用設定"""
    return Settings(
        gemini_api_key="test_api_key",
        gemini_model="gemini-1.5-pro"
    )


@pytest.fixture
def mock_model():
    """Geminiモデルのモック"""
    mock_model = Mock()
    mock_response = Mock()
    mock_response.text = "テスト応答"
    mock_model.generate_content.return_value = mock_response
    return mock_model


def test_gemini_service_init_success(mock_settings):
    """Geminiサービスの初期化成功テスト"""
    with patch('app.services.gemini_service.genai') as mock_genai:
        mock_model = Mock()
        mock_genai.GenerativeModel.return_value = mock_model
        
        service = GeminiService(mock_settings)
        
        assert service.settings == mock_settings
        mock_genai.configure.assert_called_once_with(api_key="test_api_key")
        mock_genai.GenerativeModel.assert_called_once_with("gemini-1.5-pro")
        assert service.model == mock_model


def test_gemini_service_init_no_api_key():
    """APIキーがない場合の初期化失敗テスト"""
    settings = Settings(gemini_api_key=None)
    
    with pytest.raises(ValueError, match="GEMINI_API_KEY is not configured"):
        GeminiService(settings)


@pytest.mark.asyncio
async def test_generate_response_success(mock_settings, mock_model):
    """応答生成成功テスト"""
    with patch('app.services.gemini_service.genai') as mock_genai:
        mock_genai.GenerativeModel.return_value = mock_model
        
        service = GeminiService(mock_settings)
        result = await service.generate_response("テストメッセージ")
        
        assert result == "テスト応答"
        mock_model.generate_content.assert_called_once_with("テストメッセージ")


@pytest.mark.asyncio
async def test_generate_response_with_context(mock_settings, mock_model):
    """コンテキスト付き応答生成テスト"""
    with patch('app.services.gemini_service.genai') as mock_genai:
        mock_genai.GenerativeModel.return_value = mock_model
        
        service = GeminiService(mock_settings)
        result = await service.generate_response("メッセージ", "コンテキスト")
        
        assert result == "テスト応答"
        expected_prompt = "コンテキスト: コンテキスト\n\nメッセージ: メッセージ"
        mock_model.generate_content.assert_called_once_with(expected_prompt)


@pytest.mark.asyncio
async def test_generate_response_empty_response(mock_settings):
    """空レスポンスのテスト"""
    with patch('app.services.gemini_service.genai') as mock_genai:
        mock_model = Mock()
        mock_response = Mock()
        mock_response.text = ""
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model
        
        service = GeminiService(mock_settings)
        result = await service.generate_response("テストメッセージ")
        
        assert result == "申し訳ありません。応答を生成できませんでした。"


@pytest.mark.asyncio
async def test_generate_response_api_error(mock_settings):
    """APIエラーのテスト"""
    with patch('app.services.gemini_service.genai') as mock_genai:
        mock_model = Mock()
        mock_model.generate_content.side_effect = Exception("API Error")
        mock_genai.GenerativeModel.return_value = mock_model
        
        service = GeminiService(mock_settings)
        
        with pytest.raises(GeminiAPIException, match="Gemini API呼び出しに失敗しました"):
            await service.generate_response("テストメッセージ")


def test_health_check_success(mock_settings):
    """ヘルスチェック成功テスト"""
    with patch('app.services.gemini_service.genai') as mock_genai:
        mock_model = Mock()
        mock_model.generate_content.return_value = Mock()
        mock_genai.GenerativeModel.return_value = mock_model
        
        service = GeminiService(mock_settings)
        result = service.health_check()
        
        assert result is True
        mock_model.generate_content.assert_called_once_with("test")


def test_health_check_failure(mock_settings):
    """ヘルスチェック失敗テスト"""
    with patch('app.services.gemini_service.genai') as mock_genai:
        mock_model = Mock()
        mock_model.generate_content.side_effect = Exception("Health check failed")
        mock_genai.GenerativeModel.return_value = mock_model
        
        service = GeminiService(mock_settings)
        result = service.health_check()
        
        assert result is False
