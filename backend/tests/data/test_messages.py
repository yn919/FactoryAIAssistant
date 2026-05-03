"""Test message data"""

# Messages for Gemini service tests
GEMINI_TEST_MESSAGES = {
    "simple": "Test message",
    "with_context": "Message",
    "context": "Context",
    "health_check": "test",
    "empty_response": "",
    "expected_prompt": "Context: Context\n\nMessage: Message"
}

# Messages for exception tests
EXCEPTION_TEST_MESSAGES = {
    "factory_ai": "Test message",
    "gemini_api": "API Error",
    "validation": "Validation Error",
    "configuration": "Config Error",
    "unexpected": "Unexpected error",
    "internal_server": "Internal server error occurred"
}

# Data for logging tests
LOGGING_TEST_DATA = {
    "default_level": "INFO",
    "debug_level": "DEBUG",
    "log_format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "test_logger_name": "test_logger"
}

# Data for configuration tests
CONFIG_TEST_DATA = {
    "default_values": {
        "gemini_api_key": None,
        "server_host": "0.0.0.0",
        "server_port": 8000,
        "cors_origins": ["*"],
        "cors_allow_credentials": True,
        "cors_allow_methods": ["*"],
        "cors_allow_headers": ["*"],
        "log_level": "INFO",
        "log_format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "app_name": "Factory AI Assistant API",
        "app_version": "1.0.0",
        "app_description": "Gemini AI assistant API for Unity app integration",
        "environment": "development",
        "debug": False,
        "gemini_model": "gemini-1.5-pro",
        "gemini_temperature": None,
        "gemini_max_tokens": None
    },
    "test_values": {
        "gemini_api_key": "mock_test_api_key_12345",
        "server_host": "localhost",
        "server_port": 3000,
        "environment": "test"
    },
    "mock_api_key": "mock_test_api_key_12345",
    "env_key": "env_test_key"
}
