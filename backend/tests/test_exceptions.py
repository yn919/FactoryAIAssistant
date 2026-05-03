"""Tests for exception classes"""
import pytest
from app.core.exceptions import (
    FactoryAIException,
    GeminiAPIException,
    ValidationException,
    ConfigurationException
)
from tests.data.test_messages import EXCEPTION_TEST_MESSAGES


def test_factory_ai_exception_default():
    """Test FactoryAIException default values"""
    exc = FactoryAIException(EXCEPTION_TEST_MESSAGES["factory_ai"])
    
    assert exc.message == EXCEPTION_TEST_MESSAGES["factory_ai"]
    assert exc.status_code == 500
    assert exc.details == {}
    assert str(exc) == EXCEPTION_TEST_MESSAGES["factory_ai"]


def test_factory_ai_exception_with_params():
    """Test FactoryAIException with parameters"""
    details = {"error": "test"}
    exc = FactoryAIException(EXCEPTION_TEST_MESSAGES["factory_ai"], status_code=400, details=details)
    
    assert exc.message == EXCEPTION_TEST_MESSAGES["factory_ai"]
    assert exc.status_code == 400
    assert exc.details == details


def test_gemini_api_exception():
    """Test GeminiAPIException"""
    exc = GeminiAPIException(EXCEPTION_TEST_MESSAGES["gemini_api"])
    
    assert exc.message == EXCEPTION_TEST_MESSAGES["gemini_api"]
    assert exc.status_code == 503
    assert exc.details == {}


def test_gemini_api_exception_with_details():
    """Test GeminiAPIException with details"""
    details = {"api_response": "error"}
    exc = GeminiAPIException(EXCEPTION_TEST_MESSAGES["gemini_api"], details=details)
    
    assert exc.message == EXCEPTION_TEST_MESSAGES["gemini_api"]
    assert exc.status_code == 503
    assert exc.details == details


def test_validation_exception():
    """Test ValidationException"""
    exc = ValidationException(EXCEPTION_TEST_MESSAGES["validation"])
    
    assert exc.message == EXCEPTION_TEST_MESSAGES["validation"]
    assert exc.status_code == 422
    assert exc.details == {}


def test_configuration_exception():
    """Test ConfigurationException"""
    exc = ConfigurationException(EXCEPTION_TEST_MESSAGES["configuration"])
    
    assert exc.message == EXCEPTION_TEST_MESSAGES["configuration"]
    assert exc.status_code == 500
    assert exc.details == {}
