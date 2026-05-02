"""例外クラスのテスト"""
import pytest
from app.core.exceptions import (
    FactoryAIException,
    GeminiAPIException,
    ValidationException,
    ConfigurationException
)


def test_factory_ai_exception_default():
    """FactoryAIExceptionデフォルト値テスト"""
    exc = FactoryAIException("Test message")
    
    assert exc.message == "Test message"
    assert exc.status_code == 500
    assert exc.details == {}
    assert str(exc) == "Test message"


def test_factory_ai_exception_with_params():
    """FactoryAIExceptionパラメータ付きテスト"""
    details = {"error": "test"}
    exc = FactoryAIException("Test message", status_code=400, details=details)
    
    assert exc.message == "Test message"
    assert exc.status_code == 400
    assert exc.details == details


def test_gemini_api_exception():
    """GeminiAPIExceptionテスト"""
    exc = GeminiAPIException("API Error")
    
    assert exc.message == "API Error"
    assert exc.status_code == 503
    assert exc.details == {}


def test_gemini_api_exception_with_details():
    """GeminiAPIException詳細付きテスト"""
    details = {"api_response": "error"}
    exc = GeminiAPIException("API Error", details=details)
    
    assert exc.message == "API Error"
    assert exc.status_code == 503
    assert exc.details == details


def test_validation_exception():
    """ValidationExceptionテスト"""
    exc = ValidationException("Validation Error")
    
    assert exc.message == "Validation Error"
    assert exc.status_code == 422
    assert exc.details == {}


def test_configuration_exception():
    """ConfigurationExceptionテスト"""
    exc = ConfigurationException("Config Error")
    
    assert exc.message == "Config Error"
    assert exc.status_code == 500
    assert exc.details == {}
