import asyncio
import uuid
from app.domain.models.citizen_request import GeoLocation
from app.application.use_cases.process_request import ProcessCitizenRequestUseCase
from app.infrastructure.repositories.firestore_repo import FirestoreCitizenRepository
from app.infrastructure.ai.gemini_client import GeminiAIClient

async def main():
    # Setup
    repo = FirestoreCitizenRepository()
    ai_client = GeminiAIClient()
    use_case = ProcessCitizenRequestUseCase(repo, ai_client)

    # Mock Multilingual Data
    mock_data = [
        {
            "text": "हमारे गाँव में पानी की बहुत समस्या है, पाइपलाइन टूटी हुई है।", 
            "lang": "hi", 
            "loc": {"latitude": 28.6, "longitude": 77.2, "state": "Delhi", "district": "Central"}
        },
        {
            "text": "The road to the primary school is completely washed away after the rains.", 
            "lang": "en", 
            "loc": {"latitude": 12.9, "longitude": 77.5, "state": "Karnataka", "district": "Bangalore"}
        },
        {
            "text": "आमच्या गावात आरोग्य केंद्राची खूप गरज आहे.", 
            "lang": "mr", 
            "loc": {"latitude": 19.0, "longitude": 72.8, "state": "Maharashtra", "district": "Mumbai"}
        }
    ]

    print("Starting batch ingestion...")
    for item in mock_data:
        try:
            res = await use_case.execute(item["text"], item["lang"], GeoLocation(**item["loc"]))
            print(f"Processed: {res.request_id} | Category: {res.category} | Priority: {res.priority}")
        except Exception as e:
            print(f"Failed to process {item['text'][:20]}... : {e}")

if __name__ == "__main__":
    asyncio.run(main())
