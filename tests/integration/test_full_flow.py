import asyncio
import requests
import json
from loguru import logger

API_BASE = "http://localhost:8000"

async def run_demo():
    logger.info("Starting Jan-Sunwai AI End-to-End Demo...")

    # 1. Sample Multilingual Feedback
    samples = [
        {
            "text": "sadak kharab hai, bahut gaddhe hain", # Road is bad, many potholes
            "language": "hi",
            "location": {"latitude": 28.6139, "longitude": 77.2090, "state": "Delhi", "district": "New Delhi"}
        },
        {
            "text": "paani nahi aa raha do din se", # Water not coming for 2 days
            "language": "hi",
            "location": {"latitude": 28.6140, "longitude": 77.2091, "state": "Delhi", "district": "New Delhi"}
        },
        {
            "text": "The street lights in our colony are not working, it is unsafe at night",
            "language": "en",
            "location": {"latitude": 12.9716, "longitude": 77.5946, "state": "Karnataka", "district": "Bangalore"}
        },
    ]

    logger.info("Submitting citizen requests...")
    for i, s in enumerate(samples):
        try:
            res = requests.post(f"{API_BASE}/requests", json=s)
            if res.status_code == 200:
                logger.info(f"Successfully submitted request {i+1}: {res.json().get('request_id')}")
            else:
                logger.error(f"Failed to submit request {i+1}: {res.status_code} - {res.text}")
        except Exception as e:
            logger.error(f"Request {i+1} error: {str(e)}")

    # 2. Trigger AI Policy Recommendation
    logger.info("Requesting AI-powered policy recommendation...")
    try:
        # Using a sample location based on our feedback
        params = {
            "state": "Delhi",
            "district": "New Delhi",
            "category": "Infrastructure"
        }
        rec_res = requests.get(f"{API_BASE}/policymaker/recommendation", params=params)
        
        if rec_res.status_code == 200:
            data = rec_res.json()
            logger.info("--- AI RECOMMENDED POLICY ---")
            print(f"\nGap Analysis: {json.dumps(data['gap_analysis'], indent=2)}")
            print(f"\nProposal:\n{data['proposal']}")
            print("-" * 30)
        else:
            logger.error(f"Analysis failed: {rec_res.status_code} - {rec_res.text}")
    except Exception as e:
        logger.error(f"Recommendation error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(run_demo())
