from app.domain.interfaces.citizen_repo import ICitizenRequestRepository
from app.infrastructure.ai.gemini_client import GeminiAIClient
from app.domain.models.citizen_request import CitizenRequest, RequestStatus
import uuid
from datetime import datetime

class ProcessCitizenRequestUseCase:
    def __init__(self, repo: ICitizenRequestRepository, ai_client: GeminiAIClient):
        self.repo = repo
        self.ai_client = ai_client

    async def execute(self, raw_text: str, language: str, location_data: dict) -> CitizenRequest:
        # 1. Initialize Request
        request_id = str(uuid.uuid4())
        request = CitizenRequest(
            request_id=request_id,
            original_text=raw_text,
            original_language=language,
            location=location_data, # This should be validated against GeoLocation model
            status=RequestStatus.RECEIVED
        )
        await self.repo.save(request)

        try:
            # 2. AI Classification (The core intelligence)
            classification = self.ai_client.classify_request(raw_text, language)
            
            # 3. Update Request with AI Intelligence
            request.category = classification.category
            request.sub_category = classification.sub_category
            request.priority = classification.priority
            request.status = RequestStatus.PROCESSED
            request.metadata["classification_details"] = classification.dict()
            
            await self.repo.save(request)
            return request
        except Exception as e:
            await self.repo.update_status(request_id, RequestStatus.FAILED, {"error": str(e)})
            raise e
