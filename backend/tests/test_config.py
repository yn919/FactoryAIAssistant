"""Tests for configuration module"""
import pytest
from unittest.mock import patch
from app.core.config import Settings, get_settings
from tests.data.test_messages import CONFIG_TEST_DATA


def test_settings_default_values(test_settings):
    """Test default configuration values (in mock environment)"""
    # Verify mock settings have expected values
    assert test_settings.gemini_api_key == "mock_test_api_key_12345"
    assert test_settings.server_host == "localhost"  # Test value
    assert test_settings.server_port == 8000
    assert test_settings.cors_origins == ["http://localhost:3000"]  # Test value
    assert test_settings.cors_allow_credentials is True
    assert test_settings.log_level == "INFO"
    assert test_settings.app_name == "Test Factory AI Assistant API"  # Test value
    assert test_settings.app_version == "1.0.0-test"  # Test value
    assert test_settings.environment == "test"  # Test value
    assert test_settings.gemini_model == "gemini-1.5-pro"


def test_settings_with_values():
    """Test instantiation with specified configuration values"""
    test_values = CONFIG_TEST_DATA["test_values"]
    settings = Settings(**test_values)
    
    assert settings.gemini_api_key == test_values["gemini_api_key"]
    assert settings.server_host == test_values["server_host"]
    assert settings.server_port == test_values["server_port"]
    assert settings.environment == test_values["environment"]


def test_get_settings_cached():
    """Test caching functionality of get_settings function"""
    settings1 = get_settings()
    settings2 = get_settings()
    
    # Verify same instance is returned
    assert settings1 is settings2


@patch.dict('os.environ', {'GEMINI_API_KEY': CONFIG_TEST_DATA["env_key"]})
def test_settings_from_env():
    """Test loading configuration from environment variables"""
    settings = Settings()
    
    assert settings.gemini_api_key == CONFIG_TEST_DATA["env_key"]
