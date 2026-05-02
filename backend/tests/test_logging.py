"""ロギング機能のテスト"""
import pytest
from unittest.mock import Mock, patch
import logging
from app.core.logging import setup_logging, get_logger


@patch('app.core.logging.get_settings')
@patch('app.core.logging.logging.basicConfig')
@patch('app.core.logging.logging.getLogger')
def test_setup_logging_default(mock_get_logger, mock_basic_config, mock_get_settings):
    """ロギング設定デフォルト値テスト"""
    mock_settings = Mock()
    mock_settings.log_level = "INFO"
    mock_settings.log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    mock_get_settings.return_value = mock_settings
    
    mock_logger = Mock()
    mock_get_logger.return_value = mock_logger
    
    result = setup_logging()
    
    mock_basic_config.assert_called_once()
    assert mock_get_logger.call_count >= 4  # __main__ + 3サードパーティライブラリ
    assert result == mock_logger.return_value


@patch('app.core.logging.get_settings')
@patch('app.core.logging.logging.basicConfig')
@patch('app.core.logging.logging.getLogger')
def test_setup_logging_debug_level(mock_get_logger, mock_basic_config, mock_get_settings):
    """デバッグレベルでのロギング設定テスト"""
    mock_settings = Mock()
    mock_settings.log_level = "DEBUG"
    mock_settings.log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    mock_get_settings.return_value = mock_settings
    
    mock_logger = Mock()
    mock_get_logger.return_value = mock_logger
    
    setup_logging()
    
    # DEBUGレベルで設定されていることを確認
    call_args = mock_basic_config.call_args
    assert call_args[1]['level'] == logging.DEBUG


def test_get_logger():
    """ロガー取得テスト"""
    with patch('app.core.logging.logging.getLogger') as mock_get_logger:
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger
        
        result = get_logger("test_logger")
        
        assert result == mock_logger
        mock_get_logger.assert_called_once_with("test_logger")
