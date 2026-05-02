import uvicorn
import os
import sys
from dotenv import load_dotenv

# .envファイルを読み込み
load_dotenv()

def main():
    """サーバーを起動するメイン関数"""
    try:
        # 環境変数から設定を読み込み
        host = os.getenv("SERVER_HOST", "0.0.0.0")
        port = int(os.getenv("SERVER_PORT", "8000"))
        
        print(f"Starting server on {host}:{port}")
        print("API Documentation: http://localhost:8000/docs")
        print("Health Check: http://localhost:8000/health")
        
        # サーバー起動
        uvicorn.run(
            "app.main:app",
            host=host,
            port=port,
            reload=True,
            log_level="info"
        )
        
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error starting server: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
