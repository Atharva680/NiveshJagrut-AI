import logging
from google.cloud import speech
from app.core.config.settings import settings

logger = logging.getLogger(__name__)

class VoiceTranscriptionService:
    def __init__(self):
        self.client = speech.SpeechClient()

    async def transcribe_audio(self, audio_content: bytes, language_code: str) -> str:
        """
        Transcribes audio using Google Cloud Speech-to-Text.
        Support for multiple Indian languages (hi-IN, mr-IN, ta-IN, etc.)
        """
        audio = speech.RecognitionAudio(content=audio_content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code=language_code,
        )

        try:
            response = self.client.recognize(config=config, audio=audio)
            transcript = " ".join([result.alternatives[0].transcript for result in response.results])
            return transcript
        except Exception as e:
            logger.error(f"Voice transcription failed: {str(e)}")
            raise RuntimeError("Failed to transcribe audio")
