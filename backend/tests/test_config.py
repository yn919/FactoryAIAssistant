"""設定モジュールのテスト"""
import pytest
from unittest.mock import patch
from app.core.config import Settings, get_settings


def test_settings_default_values():
    """設定のデフォルト値をテスト"""
    settings = Settings()
    
    assert settings.gemini_api_key is None
    assert settings.server_host == "0.0.0.0"
    assert settings.server_port == 8000
    assert settings.cors_origins == ["*"]
    assert settings.cors_allow_credentials is True
    assert settings.log_level == "INFO"
    assert settings.app_name == "Factory AI Assistant API"
    assert settings.app_version == "1.0.0"
    assert settings.environment == "development"
    assert settings.gemini_model == "gemini-1.5-pro"


def test_settings_with_values():
    """設定値を指定してインスタンス化するテスト"""
    settings = Settings(
        gemini_api_key="test_key",
        server_host="localhost",
        server_port=3000,
        environment="test"
    )
    
    assert settings.gemini_api_key == "test_key"
    assert settings.server_host == "localhost"
    assert settings.server_port == 3000
    assert settings.environment == "test"


def test_get_settings_cached():
    """get_settings関数のキャッシュ機能をテスト"""
    settings1 = get_settings()
    settings2 = get_settings()
    
    # 同じインスタンスが返されることを確認
    assert settings1 is settings2


@patch.dict('os.environ', {'GEMINI_API_KEY': 'env_test_key'})
def test_settings_from_env():
    """環境変数から設定を読み込むテスト"""
    settings = Settings()
    
    assert settings.gemini_api_key == 'env_test_key'
