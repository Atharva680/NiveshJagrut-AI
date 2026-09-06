
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from app.domain.models.citizen_request import CitizenRequest, GeoLocation
from app.application.use_cases.process_request import ProcessCitizenRequestUseCase
from app.infrastructure.repositories.firestore_repo import FirestoreCitizenRepository
from app.infrastructure.ai.gemini_client import GeminiAIClient
from app.infrastructure.external.gap_engine import InfrastructureGapEngine
from pydantic import BaseModel
import uuid

app = FastAPI(title="CivicIntelligence API", version="1.0.0")

# Dependency Injection
def get_process_use_case():
    return ProcessCitizenRequestUseCase(FirestoreCitizenRepository(), GeminiAIClient())

def get_ai_client():
    return GeminiAIClient()

def get_gap_engine():
    return InfrastructureGapEngine()

class RequestInput(BaseModel):
    text: str
    language: str
    location: GeoLocation

@app.post("/requests", response_model=CitizenRequest)
async def create_request(payload: RequestInput, use_case: ProcessCitizenRequestUseCase = Depends(get_process_use_case)):
    return await use_case.execute(payload.text, payload.language, payload.location)

@app.post("/requests/multimodal")
async def create_multimodal_request(
    text: str, 
    language: str, 
    location: GeoLocation, 
    file: UploadFile = File(...), 
    ai_client: GeminiAIClient = Depends(get_ai_client)
):
    # 1. Handle File (Image)
    image_bytes = await file.read()
    vision_result = ai_client.analyze_infrastructure_image(image_bytes, text)
    
    # 2. Process as standard request
    use_case = ProcessCitizenRequestUseCase(FirestoreCitizenRepository(), ai_client)
    request = await use_case.execute(text, language, location)
    
    # 3. Attach Vision Verification
    request.metadata["vision_verification"] = vision_result
    await FirestoreCitizenRepository().save(request)
    
    return request

@app.get("/policymaker/recommendation")
async def get_recommendation(state: str, district: str, category: str, gap_engine: InfrastructureGapEngine = Depends(get_gap_engine), ai_client: GeminiAIClient = Depends(get_ai_client)):
    # 1. Analyze the gap
    gap_report = await gap_engine.analyze_regional_gap(state, district, category)
    
    # 2. Generate AI-powered policy proposal
    proposal = ai_client.generate_policy_recommendation(gap_report)
    
    return {
        "gap_analysis": gap_report,
        "proposal": proposal
    }
