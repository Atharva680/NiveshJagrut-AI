import asyncio
import requests
from loguru import logger

API_BASE = "http://localhost:8000"

async def run_demo():
    logger.info("Starting Jan-Sunwai AI End-to-End Demo...")

    # 1. Sample Multilingual Feedback (Real-world scenarios)
    samples = [
        {
            "citizen_id": "CIT-001",
            "language": "hi",
            "content": "sadak kharab hai, bahut gaddhe hain", # Road is bad, many potholes
            "channel": "text",
            "lat": 28.6139, "lng": 77.2090, "pincode": "110001"
        },
        {
            "citizen_id": "CIT-002",
            "language": "hi",
            "content": "paani nahi aa raha do din se", # Water not coming for 2 days
            "channel": "text",
            "lat": 28.6140, "lng": 77.2091, "pincode": "110001"
        },
        {
            "citizen_id": "CIT-003",
            "language": "en",
            "content": "The street lights in our colony are not working, it is unsafe at night",
            "channel": "text",
            "lat": 12.9716, "lng": 77.5946, "pincode": "560001"
        },
        {
            "citizen_id": "CIT-004",
            "language": "hi",
            "content": "sadak par bahut gaddhe hain, accident ho rahe hain", # Potholes on road, accidents happening
            "channel": "text",
            "lat": 28.6135, "lng": 77.2085, "pincode": "110001"
        },
    ]

    logger.info("Submitting citizen feedback...")
    for s in samples:
        res = requests.post(f"{API_BASE}/feedback/submit", data=s)
        if res.status_code == 200:
            logger.info(f"Successfully submitted feedback for {s['citizen_id']}")
        else:
            logger.error(f"Failed to submit {s['citizen_id']}: {res.text}")

    # 2. Trigger AI Synthesis
    logger.info("Requesting AI-powered project recommendations...")
    rec_res = requests.get(f"{API_BASE}/analytics/recommendations")
    
    if rec_res.status_code == 200:
        recs = rec_res.json()
        logger.info("--- AI RECOMMENDED PROJECTS ---")
        for r in recs:
            print(f"\nProject: {r['title']}")
            print(f"Priority: {r['priority_score']}/100")
            print(f"Justification: {r['justification']}")
            print(f"Est. Cost: ₹{r['estimated_cost']}")
            print("-" * 30)
    else:
        logger.error(f"Analysis failed: {rec_res.text}")

if __name__ == "__main__":
    asyncio.run(run_demo())
