import pytest
import sys
import os
from unittest.mock import Mock, AsyncMock, patch

# モジュールパスを追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# テスト環境では.envファイルを読み込まないように設定
@pytest.fixture(autouse=True)
def mock_env_settings():
    """テスト環境用のモック設定"""
    with patch.dict(os.environ, {
        'GEMINI_API_KEY': 'test_api_key',
        'SERVER_HOST': 'localhost',
        'SERVER_PORT': '8000'
    }):
        yield

@pytest.fixture
def mock_gemini_response():
    """Gemini APIのモックレスポンス"""
    mock_response = Mock()
    mock_response.text = "これはテスト応答です"
    return mock_response

@pytest.fixture
def mock_gemini_service():
    """Geminiサービスのモック"""
    from app.services.gemini_service import GeminiService
    
    mock_service = Mock(spec=GeminiService)
    mock_service.generate_response = AsyncMock(return_value="テスト応答メッセージ")
    mock_service.health_check = Mock(return_value=True)
    return mock_service

@pytest.fixture(autouse=True)
def mock_gemini_service_import():
    """Geminiサービスのインポートをモック"""
    mock_service = Mock()
    mock_service.generate_response = AsyncMock(return_value="モック応答")
    mock_service.health_check = Mock(return_value=True)
    
    with patch('app.main.gemini_service', mock_service):
        yield
