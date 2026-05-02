import pytest
import sys
import os
from unittest.mock import Mock, AsyncMock

# モジュールパスを追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
