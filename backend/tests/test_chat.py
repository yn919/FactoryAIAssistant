import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, Mock
import sys
import os

# モジュールパスを追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from tests.fixtures.gemini_service import test_settings, mock_gemini_service

# テスト用のクライアントを作成
def create_test_client():
    """モックを注入したテストクライアントを作成"""
    from app.core.dependencies import get_gemini_service
    
    def override_get_gemini_service():
        mock_service = Mock()
        mock_service.generate_response = AsyncMock(return_value="テスト応答メッセージ")
        mock_service.health_check = Mock(return_value=True)
        return mock_service
    
    app.dependency_overrides[get_gemini_service] = override_get_gemini_service
    client = TestClient(app)
    
    # テスト後にオーバーライドをクリーンアップ
    def cleanup():
        app.dependency_overrides.clear()
    
    return client, cleanup

def test_health_endpoint():
    """ヘルスチェックエンドポイントのテスト"""
    client, cleanup = create_test_client()
    try:
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    finally:
        cleanup()

def test_root_endpoint():
    """ルートエンドポイントのテスト"""
    client, cleanup = create_test_client()
    try:
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()
    finally:
        cleanup()

def test_chat_endpoint_success():
    """正常なチャットリクエストのテスト"""
    client, cleanup = create_test_client()
    try:
        response = client.post(
            "/api/v1/chat",
            json={"message": "こんにちは"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert data["response"] == "テスト応答メッセージ"
    finally:
        cleanup()

def test_chat_endpoint_empty_message():
    """空メッセージのエラーテスト"""
    client, cleanup = create_test_client()
    try:
        response = client.post(
            "/api/v1/chat",
            json={"message": ""}
        )
        
        assert response.status_code == 422  # Validation error
    finally:
        cleanup()

def test_chat_endpoint_missing_message():
    """メッセージフィールドがない場合のエラーテスト"""
    client, cleanup = create_test_client()
    try:
        response = client.post(
            "/api/v1/chat",
            json={}
        )
        
        assert response.status_code == 422  # Validation error
    finally:
        cleanup()

def test_chat_endpoint_with_context():
    """コンテキスト付きチャットリクエストのテスト"""
    client, cleanup = create_test_client()
    try:
        response = client.post(
            "/api/v1/chat",
            json={
                "message": "質問です",
                "context": "これはテストコンテキストです"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert data["response"] == "テスト応答メッセージ"
    finally:
        cleanup()

def test_chat_endpoint_service_error():
    """サービスエラー時のテスト"""
    from app.core.exceptions import GeminiAPIException
    from app.core.dependencies import get_gemini_service
    
    def override_get_gemini_service_error():
        mock_service = Mock()
        mock_service.generate_response = AsyncMock(side_effect=GeminiAPIException("APIエラー"))
        mock_service.health_check = Mock(return_value=True)
        return mock_service
    
    app.dependency_overrides[get_gemini_service] = override_get_gemini_service_error
    client = TestClient(app)
    
    try:
        response = client.post(
            "/api/v1/chat",
            json={"message": "こんにちは"}
        )
        
        assert response.status_code == 503
    finally:
        app.dependency_overrides.clear()

def test_chat_endpoint_long_message():
    """長すぎるメッセージのバリデーションテスト"""
    client, cleanup = create_test_client()
    try:
        long_message = "a" * 1001  # 1000文字を超えるメッセージ
        
        response = client.post(
            "/api/v1/chat",
            json={"message": long_message}
        )
        
        assert response.status_code == 422  # Validation error
    finally:
        cleanup()

def test_chat_endpoint_long_context():
    """長すぎるコンテキストのバリデーションテスト"""
    client, cleanup = create_test_client()
    try:
        long_context = "a" * 501  # 500文字を超えるコンテキスト
        
        response = client.post(
            "/api/v1/chat",
            json={
                "message": "テスト",
                "context": long_context
            }
        )
        
        assert response.status_code == 422  # Validation error
    finally:
        cleanup()
