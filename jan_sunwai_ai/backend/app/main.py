from fastapi import FastAPI, UploadFile, File, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import shutil
import os
from loguru import logger

from app.core.config import settings
from app.models.domain import CitizenFeedback, FeedbackChannel, ProjectRecommendation
from app.services.feedback_manager import FeedbackService
from app.services.translation import MockTranslationService
from app.services.speech import MockSpeechProcessor
from app.services.analysis_engine import AnalysisEngine
from app.core.mock_data import MockDataGenerator

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencies
translation_service = MockTranslationService()
speech_processor = MockSpeechProcessor(credentials_path=settings.GOOGLE_APPLICATION_CREDENTIALS)
feedback_service = FeedbackService(translation_service, speech_processor)
analysis_engine = AnalysisEngine()

# In-memory storage for prototype
feedback_db = []

@app.post("/feedback/submit")
async def submit_feedback(
    citizen_id: str = Form(...),
    language: str = Form(...),
    content: Optional[str] = Form(None),
    channel: FeedbackChannel = Form(...),
    lat: float = Form(...),
    lng: float = Form(...),
    pincode: str = Form(...),
    audio: Optional[UploadFile] = File(None)
):
    # Create domain model
    feedback = CitizenFeedback(
        citizen_id=citizen_id,
        language=language,
        original_content=content or "",
        channel=channel,
        location={"lat": lat, "lng": lng},
        pincode=pincode
    )

    audio_path = None
    if audio:
        audio_path = f"temp_{audio.filename}"
        with open(audio_path, "wb") as buffer:
            shutil.copyfileobj(audio.file, buffer)

    # Process via multimodal pipeline
    processed_feedback = await feedback_service.process_feedback(feedback, audio_path)
    
    # Simple categorization (in production, this would be another Gemini call)
    if "road" in processed_feedback.translated_content.lower():
        processed_feedback.category = "Infrastructure-Roads"
    elif "water" in processed_feedback.translated_content.lower():
        processed_feedback.category = "Infrastructure-Water"
    else:
        processed_feedback.category = "General"

    feedback_db.append(processed_feedback)
    
    # Cleanup audio
    if audio_path and os.path.exists(audio_path):
        os.remove(audio_path)

    return {"status": "success", "feedback_id": processed_feedback.id}

@app.get("/analytics/recommendations", response_model=List[ProjectRecommendation])
async def get_recommendations():
    # 1. Get sample infra data
    infra_data = MockDataGenerator.get_sample_infrastructure()
    
    # 2. Analyze current feedback pool using Gemini
    recommendations = await analysis_engine.synthesize_feedback_and_recommend(
        feedback_db, 
        infra_data
    )
    
    return recommendations

@app.get("/feedback/all")
async def get_all_feedback():
    return feedback_db

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
