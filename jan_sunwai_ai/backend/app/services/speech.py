from abc import ABC, abstractmethod
from typing import Optional
import os

class ISpeechProcessor(ABC):
    @abstractmethod
    async def speech_to_text(self, audio_file_path: str, language_code: Optional[str] = None) -> str:
        pass

class GoogleSpeechProcessor(ISpeechProcessor):
    def __init__(self, credentials_path: str):
        self.credentials_path = credentials_path

    async def speech_to_text(self, audio_file_path: str, language_code: Optional[str] = None) -> str:
        # In production:
        # client = speech.SpeechClient()
        # response = client.recognize(...)
        return "Sample transcribed text from Google STT"

class MockSpeechProcessor(ISpeechProcessor):
    async def speech_to_text(self, audio_file_path: str, language_code: Optional[str] = None) -> str:
        # Simulate transcription based on file name for the demo
        if "road" in audio_file_path:
            return "sadak kharab hai"
        if "water" in audio_file_path:
            return "paani nahi aa raha"
        return "general complaint about public services"
