import logging
import sys
from app.core.config import get_settings


def setup_logging():
    """構造化ロギングの設定"""
    settings = get_settings()
    
    # ロガーの基本設定
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format=settings.log_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.StreamHandler(sys.stderr)
        ]
    )
    
    # サードパーティライブラリのログレベルを調整
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("fastapi").setLevel(logging.INFO)
    logging.getLogger("google.generativeai").setLevel(logging.WARNING)
    
    return logging.getLogger(__name__)


def get_logger(name: str) -> logging.Logger:
    """ロガーインスタンスの取得"""
    return logging.getLogger(name)
