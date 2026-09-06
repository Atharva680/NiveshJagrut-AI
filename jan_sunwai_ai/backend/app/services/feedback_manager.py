from app.models.domain import CitizenFeedback, FeedbackStatus
from app.services.translation import ITranslationService
from app.services.speech import ISpeechProcessor
from loguru import logger
import uuid

class FeedbackService:
    def __init__(self, translation_service: ITranslationService, speech_processor: ISpeechProcessor):
        self.translation_service = translation_service
        self.speech_processor = speech_processor

    async def process_feedback(self, feedback: CitizenFeedback, audio_path: Optional[str] = None) -> CitizenFeedback:
        logger.info(f"Processing feedback from citizen {feedback.citizen_id}")

        # 1. Handle Multimodal Input (Speech to Text)
        if feedback.channel == "voice" and audio_path:
            logger.info("Converting speech to text...")
            feedback.original_content = await self.speech_processor.speech_to_text(audio_path, feedback.language)
        
        # 2. Language Detection and Translation
        detected_lang = await self.translation_service.detect_language(feedback.original_content)
        feedback.language = detected_lang
        
        if detected_lang != "en":
            logger.info(f"Translating from {detected_lang} to en...")
            feedback.translated_content = await self.translation_service.translate(feedback.original_content, "en")
        else:
            feedback.translated_content = feedback.original_content

        # 3. Update Status
        feedback.status = FeedbackStatus.PROCESSED
        feedback.id = str(uuid.uuid4())
        
        return feedback
