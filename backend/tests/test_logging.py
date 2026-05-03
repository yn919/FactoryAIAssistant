"""Tests for logging functionality"""
import pytest
from unittest.mock import patch
import logging
from app.core.logging import setup_logging, get_logger
from tests.data.test_messages import LOGGING_TEST_DATA


@patch('app.core.logging.get_settings')
@patch('app.core.logging.logging.basicConfig')
@patch('app.core.logging.logging.getLogger')
def test_setup_logging_default(mock_get_logger, mock_basic_config, mock_get_settings):
    """Test logging configuration default values"""
    mock_settings = mock_get_settings.return_value
    mock_settings.log_level = LOGGING_TEST_DATA["default_level"]
    mock_settings.log_format = LOGGING_TEST_DATA["log_format"]
    
    mock_logger = mock_get_logger.return_value
    
    result = setup_logging()
    
    mock_basic_config.assert_called_once()
    assert mock_get_logger.call_count >= 4  # __main__ + 3 third-party libraries
    assert result == mock_logger


@patch('app.core.logging.get_settings')
@patch('app.core.logging.logging.basicConfig')
@patch('app.core.logging.logging.getLogger')
def test_setup_logging_debug_level(mock_get_logger, mock_basic_config, mock_get_settings):
    """Test logging configuration at debug level"""
    mock_settings = mock_get_settings.return_value
    mock_settings.log_level = LOGGING_TEST_DATA["debug_level"]
    mock_settings.log_format = LOGGING_TEST_DATA["log_format"]
    
    mock_logger = mock_get_logger.return_value
    
    setup_logging()
    
    # Verify configured at DEBUG level
    call_args = mock_basic_config.call_args
    assert call_args[1]['level'] == logging.DEBUG


def test_get_logger():
    """Test logger retrieval"""
    with patch('app.core.logging.logging.getLogger') as mock_get_logger:
        mock_logger = mock_get_logger.return_value
        
        result = get_logger(LOGGING_TEST_DATA["test_logger_name"])
        
        assert result == mock_logger
        mock_get_logger.assert_called_once_with(LOGGING_TEST_DATA["test_logger_name"])
