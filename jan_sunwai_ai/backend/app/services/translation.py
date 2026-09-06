from abc import ABC, abstractmethod
from typing import List

class ITranslationService(ABC):
    @abstractmethod
    async def translate(self, text: str, target_lang: str = "en") -> str:
        pass

    @abstractmethod
    async def detect_language(self, text: str) -> str:
        pass

class GoogleTranslateService(ITranslationService):
    def __init__(self, api_key: str):
        self.api_key = api_key
        # In production, we would use google-cloud-translate client here

    async def translate(self, text: str, target_lang: str = "en") -> str:
        # Real implementation would call Google Cloud Translation API
        # For the prototype, we simulate the network call
        return f"[Translated to {target_lang}]: {text}"

    async def detect_language(self, text: str) -> str:
        # Real implementation would call detect_language
        return "hi" # Defaulting to Hindi for prototype samples

class MockTranslationService(ITranslationService):
    async def translate(self, text: str, target_lang: str = "en") -> str:
        # Mock translations for common Indian language samples
        mocks = {
            "sadak kharab hai": "the road is in bad condition",
            "paani nahi aa raha": "water is not coming",
            "bijli kat gayi": "electricity is cut off",
        }
        return mocks.get(text.lower(), f"[Mock Translation]: {text}")

    async def detect_language(self, text: str) -> str:
        return "hi"
