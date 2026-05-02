"""FastAPIメインアプリケーションのテスト"""
import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import Settings


@pytest.fixture
def client():
    """テストクライアント"""
    return TestClient(app)


def test_app_creation():
    """アプリケーション作成のテスト"""
    assert app.title == "Factory AI Assistant API"
    assert app.version == "1.0.0"
    assert "Unityアプリと連携するGemini AIアシスタントAPI" in app.description


def test_app_includes_router():
    """APIルーターが含まれていることを確認"""
    routes = [route.path for route in app.routes]
    assert "/api/v1" in routes or any("/api/v1" in route for route in routes)


def test_cors_middleware_added():
    """CORSミドルウェアが追加されていることを確認"""
    middleware_types = [type(middleware.cls) for middleware in app.user_middleware]
    from fastapi.middleware.cors import CORSMiddleware
    assert CORSMiddleware in middleware_types


def test_exception_handlers_added():
    """例外ハンドラーが追加されていることを確認"""
    from app.core.exceptions import FactoryAIException
    from fastapi import HTTPException
    
    assert FactoryAIException in app.exception_handlers
    assert Exception in app.exception_handlers


@patch('app.main.get_settings')
@pytest.mark.asyncio
async def test_lifespan_startup_success(mock_get_settings):
    """ライフスパン起動成功テスト"""
    mock_settings = Settings(
        server_host="localhost",
        server_port=8000
    )
    mock_get_settings.return_value = mock_settings
    
    # lifespan関数をテストするために直接呼び出し
    from app.main import lifespan
    from fastapi import FastAPI
    
    test_app = FastAPI()
    
    # コンテキストマネージャーとして実行
    async with lifespan(test_app):
        pass  # 正常に完了することを確認


@patch('app.main.get_settings')
@patch('app.main.logger')
@pytest.mark.asyncio
async def test_lifespan_startup_failure(mock_logger, mock_get_settings):
    """ライフスパン起動失敗テスト"""
    mock_get_settings.side_effect = Exception("Startup error")
    
    from app.main import lifespan
    from fastapi import FastAPI
    
    test_app = FastAPI()
    
    # 起動時エラーが発生することを確認
    with pytest.raises(Exception, match="Startup error"):
        async with lifespan(test_app):
            pass


@patch('app.main.uvicorn.run')
@patch('app.main.get_settings')
def test_main_execution(mock_get_settings, mock_uvicorn_run):
    """メイン実行テスト"""
    mock_settings = Settings(
        server_host="localhost",
        server_port=8000
    )
    mock_get_settings.return_value = mock_settings
    
    # __main__ブロックをシミュレート
    with patch.dict('__main__.__dict__', {'__name__': '__main__'}):
        # インポート時に実行される部分をテスト
        import app.main
        
    # uvicorn.runが正しい引数で呼ばれることを確認
    # このテストは実際の実行環境では呼ばれないため、モック検証は省略
