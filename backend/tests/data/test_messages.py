"""テスト用メッセージデータ"""

# Geminiサービステスト用メッセージ
GEMINI_TEST_MESSAGES = {
    "simple": "テストメッセージ",
    "with_context": "メッセージ",
    "context": "コンテキスト",
    "health_check": "test",
    "empty_response": "",
    "expected_prompt": "コンテキスト: コンテキスト\n\nメッセージ: メッセージ"
}

# 例外テスト用メッセージ
EXCEPTION_TEST_MESSAGES = {
    "factory_ai": "Test message",
    "gemini_api": "API Error",
    "validation": "Validation Error",
    "configuration": "Config Error",
    "unexpected": "Unexpected error",
    "internal_server": "内部サーバーエラーが発生しました"
}

# ロギングテスト用データ
LOGGING_TEST_DATA = {
    "default_level": "INFO",
    "debug_level": "DEBUG",
    "log_format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "test_logger_name": "test_logger"
}

# 設定テスト用データ
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
        "app_description": "Unityアプリと連携するGemini AIアシスタントAPI",
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
