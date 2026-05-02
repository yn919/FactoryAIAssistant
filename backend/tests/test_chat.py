import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
import sys
import os

# モジュールパスを追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app

client = TestClient(app)

def test_health_endpoint():
    """ヘルスチェックエンドポイントのテスト"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] in ["healthy", "unhealthy"]

def test_root_endpoint():
    """ルートエンドポイントのテスト"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

@patch('app.main.gemini_service')
def test_chat_endpoint_success(mock_gemini):
    """正常なチャットリクエストのテスト"""
    # モックの設定
    mock_gemini.generate_response = AsyncMock(return_value="こんにちは！何かお手伝いできますか？")
    mock_gemini.health_check = Mock(return_value=True)
    
    response = client.post(
        "/chat",
        json={"message": "こんにちは"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "timestamp" in data
    assert data["response"] == "こんにちは！何かお手伝いできますか？"

def test_chat_endpoint_empty_message():
    """空メッセージのエラーテスト"""
    response = client.post(
        "/chat",
        json={"message": ""}
    )
    
    assert response.status_code == 422  # Validation error

def test_chat_endpoint_missing_message():
    """メッセージフィールドがない場合のエラーテスト"""
    response = client.post(
        "/chat",
        json={}
    )
    
    assert response.status_code == 422  # Validation error

@patch('app.main.gemini_service')
def test_chat_endpoint_with_context(mock_gemini):
    """コンテキスト付きチャットリクエストのテスト"""
    # モックの設定
    mock_gemini.generate_response = AsyncMock(return_value="コンテキストを考慮した応答")
    mock_gemini.health_check = Mock(return_value=True)
    
    response = client.post(
        "/chat",
        json={
            "message": "質問です",
            "context": "これはテストコンテキストです"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert data["response"] == "コンテキストを考慮した応答"

@patch('app.main.gemini_service')
def test_chat_endpoint_service_error(mock_gemini):
    """サービスエラー時のテスト"""
    # モックで例外を発生
    mock_gemini.generate_response = AsyncMock(side_effect=Exception("APIエラー"))
    mock_gemini.health_check = Mock(return_value=True)
    
    response = client.post(
        "/chat",
        json={"message": "こんにちは"}
    )
    
    assert response.status_code == 500

def test_chat_endpoint_long_message():
    """長すぎるメッセージのバリデーションテスト"""
    long_message = "a" * 1001  # 1000文字を超えるメッセージ
    
    response = client.post(
        "/chat",
        json={"message": long_message}
    )
    
    assert response.status_code == 422  # Validation error

def test_chat_endpoint_long_context():
    """長すぎるコンテキストのバリデーションテスト"""
    long_context = "a" * 501  # 500文字を超えるコンテキスト
    
    response = client.post(
        "/chat",
        json={
            "message": "テスト",
            "context": long_context
        }
    )
    
    assert response.status_code == 422  # Validation error
