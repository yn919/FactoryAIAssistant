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
        Generate chat response using Gemini API
        
        Args:
            message: User message
            context: Optional context information
            
        Returns:
            Generated AI response
        """
        try:
            # Add context to prompt if available
            full_prompt = message
            if context:
                full_prompt = f"Context: {context}\n\nMessage: {message}"
            
            # Call Gemini API
            response = self.model.generate_content(full_prompt)
            
            if response.text:
                return response.text.strip()
            else:
                logger.warning("Empty response from Gemini API")
                return "Sorry, unable to generate response."
                
        except Exception as e:
            logger.error(f"Error generating response with Gemini: {str(e)}")
            raise GeminiAPIException(f"Gemini API call failed: {str(e)}")
    
    def health_check(self) -> bool:
        """
        Gemini API health check
        
        Returns:
            True if API is available
        """
        try:
            response = self.model.generate_content("test")
            return True
        except Exception as e:
            logger.error(f"Gemini API health check failed: {str(e)}")
            return False

