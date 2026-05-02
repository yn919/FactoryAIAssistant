import google.generativeai as genai
from typing import Optional
import logging
from app.core.config import Settings
from app.core.exceptions import GeminiAPIException

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self, settings: Settings):
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is not configured")
        
        self.settings = settings
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel(settings.gemini_model)
    
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
            raise GeminiAPIException(f"Gemini API呼び出しに失敗しました: {str(e)}")
    
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

