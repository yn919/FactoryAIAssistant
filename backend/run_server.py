import uvicorn
import os
import sys
from dotenv import load_dotenv

# Load .env file
load_dotenv()

def main():
    """Main function to start server"""
    try:
        # Load configuration from environment variables
        host = os.getenv("SERVER_HOST", "0.0.0.0")
        port = int(os.getenv("SERVER_PORT", "8000"))
        
        print(f"Starting server on {host}:{port}")
        print("API Documentation: http://localhost:8000/docs")
        print("Health Check: http://localhost:8000/health")
        
        # Start server
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
