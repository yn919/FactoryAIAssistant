from fastapi import HTTPException


class FactoryAIException(Exception):
    """Factory AI Assistantの基本例外クラス"""
    
    def __init__(self, message: str, status_code: int = 500, details: dict = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class GeminiAPIException(FactoryAIException):
    """Gemini API関連の例外"""
    
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, status_code=503, details=details)


class ValidationException(FactoryAIException):
    """バリデーション関連の例外"""
    
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, status_code=422, details=details)


class ConfigurationException(FactoryAIException):
    """設定関連の例外"""
    
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, status_code=500, details=details)
