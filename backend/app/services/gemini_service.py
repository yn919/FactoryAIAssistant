import google.generativeai as genai
from typing import Optional
import logging
from app.config import settings

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not configured")
        
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    async def generate_response(self, message: str, context: Optional[str] = None) -> str:
        """
        Gemini APIを使用してチャットレスポンスを生成
        
        Args:
            message: ユーザーメッセージ
            context: オプションのコンテキスト情報
            
        Returns:
            生成されたAIレスポンス
        """
        try:
            # コンテキストがある場合はプロンプトに追加
            full_prompt = message
            if context:
                full_prompt = f"コンテキスト: {context}\n\nメッセージ: {message}"
            
            # Gemini APIを呼び出し
            response = self.model.generate_content(full_prompt)
            
            if response.text:
                return response.text.strip()
            else:
                logger.warning("Empty response from Gemini API")
                return "申し訳ありません。応答を生成できませんでした。"
                
        except Exception as e:
            logger.error(f"Error generating response with Gemini: {str(e)}")
            return "申し訳ありません。現在サービスを利用できません。しばらくしてから再度お試しください。"
    
    def health_check(self) -> bool:
        """
        Gemini APIのヘルスチェック
        
        Returns:
            APIが利用可能な場合はTrue
        """
        try:
            response = self.model.generate_content("test")
            return True
        except Exception as e:
            logger.error(f"Gemini API health check failed: {str(e)}")
            return False

# 遅延初期化用のインスタンス
_gemini_service_instance = None

def get_gemini_service():
    """GeminiServiceのインスタンスを取得（遅延初期化）"""
    global _gemini_service_instance
    if _gemini_service_instance is None:
        _gemini_service_instance = GeminiService()
    return _gemini_service_instance
