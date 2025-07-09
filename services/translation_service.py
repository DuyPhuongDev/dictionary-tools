from googletrans import Translator
import asyncio
from typing import Optional

class TranslationService:
    def __init__(self):
        self.translator = Translator()
    
    async def translate_to_vietnamese(self, text: str) -> str:
        """
        Translate English text to Vietnamese
        """
        if not text or text.strip() == "":
            return ""
        
        try:
            # Run the translation in a thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None, 
                self._translate_sync, 
                text.strip()
            )
            return result
        except Exception as e:
            print(f"Translation error for '{text}': {str(e)}")
            return f"Translation error: {text}"
    
    def _translate_sync(self, text: str) -> str:
        """
        Synchronous translation method
        """
        try:
            result = self.translator.translate(text, src='en', dest='vi')
            return result.text
        except Exception as e:
            print(f"Sync translation error: {str(e)}")
            return text  # Return original text if translation fails
    
    async def translate_batch(self, texts: list) -> list:
        """
        Translate multiple texts to Vietnamese
        """
        results = []
        for text in texts:
            translated = await self.translate_to_vietnamese(text)
            results.append(translated)
            # Small delay to avoid rate limiting
            await asyncio.sleep(0.1)
        return results 