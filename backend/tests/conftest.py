import pytest
import sys
import os
from unittest.mock import Mock, AsyncMock, patch

# モジュールパスを追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# テストフィクスチャをインポート
from tests.fixtures.gemini_service import test_settings, mock_gemini_service, mock_gemini_response
