"""Tests for CORS middleware"""
import pytest
from unittest.mock import Mock, patch
from fastapi import FastAPI
from app.middleware.cors import add_cors_middleware


@patch('app.middleware.cors.get_settings')
def test_add_cors_middleware_default(mock_get_settings):
    """Test CORS middleware addition with default settings"""
    mock_settings = Mock()
    mock_settings.cors_origins = ["*"]
    mock_settings.cors_allow_credentials = True
    mock_settings.cors_allow_methods = ["*"]
    mock_settings.cors_allow_headers = ["*"]
    mock_get_settings.return_value = mock_settings
    
    app = FastAPI()
    
    add_cors_middleware(app)
    
    # Verify middleware was added
    assert len(app.user_middleware) > 0
    
    # Verify CORSMiddleware was added
    middleware_classes = [middleware.cls for middleware in app.user_middleware]
    from starlette.middleware.cors import CORSMiddleware
    assert CORSMiddleware in middleware_classes


@patch('app.middleware.cors.get_settings')
def test_add_cors_middleware_custom_settings(mock_get_settings):
    """Test CORS middleware addition with custom settings"""
    mock_settings = Mock()
    mock_settings.cors_origins = ["http://localhost:3000"]
    mock_settings.cors_allow_credentials = False
    mock_settings.cors_allow_methods = ["GET", "POST"]
    mock_settings.cors_allow_headers = ["Content-Type"]
    mock_get_settings.return_value = mock_settings
    
    app = FastAPI()
    
    add_cors_middleware(app)
    
    # Verify middleware was added
    assert len(app.user_middleware) > 0
    
    # Verify settings were passed correctly
    middleware = app.user_middleware[0]
    assert middleware.kwargs["allow_origins"] == ["http://localhost:3000"]
    assert middleware.kwargs["allow_credentials"] is False
    assert middleware.kwargs["allow_methods"] == ["GET", "POST"]
    assert middleware.kwargs["allow_headers"] == ["Content-Type"]
