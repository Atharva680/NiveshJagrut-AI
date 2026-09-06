import google.generativeai as genai
from app.core.config import settings
from app.models.domain import CitizenFeedback, InfrastructureData, ProjectRecommendation
from typing import List, Dict
import json
from loguru import logger

class AnalysisEngine:
    def __init__(self):
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    async def synthesize_feedback_and_recommend(
        self, 
        feedback_list: List[CitizenFeedback], 
        infra_data: List[InfrastructureData]
    ) -> List[ProjectRecommendation]:
        """
        Uses Gemini to analyze citizen grievances and cross-reference them with existing 
        infrastructure data to recommend priority projects.
        """
        logger.info(f"Synthesizing {len(feedback_list)} feedback entries with {len(infra_data)} infra records")

        # Prepare data for the prompt
        feedback_summary = "\n".join([
            f"- [{f.pincode}] {f.translated_content} (Cat: {f.category})" 
            for f in feedback_list
        ])
        
        infra_summary = "\n".join([
            f"- Region {i.region_id}: {i.infrastructure_type} status: {i.current_status}, Budget: {i.budget_allocated}" 
            for i in infra_data
        ])

        prompt = f"""
        You are a Principal Public Policy Expert and Urban Planner for the Government of India.
        Your task is to analyze citizen feedback and infrastructure data to recommend high-priority public development projects.

        ### INPUT DATA:
        CITIZEN FEEDBACK:
        {feedback_summary}

        EXISTING INFRASTRUCTURE STATUS:
        {infra_summary}

        ### REQUIREMENTS:
        1. Identify recurring themes/grievances.
        2. Cross-reference grievances with existing infrastructure status (e.g., if people complain about roads AND the status is 'Critical', it's a high priority).
        3. Generate a list of recommended projects.
        4. For each project, provide a priority score (0-100) based on urgency, number of affected citizens, and current infra degradation.
        5. Output the result strictly as a JSON list of objects following this schema:
           {{
             "project_id": "string",
             "title": "string",
             "priority_score": float,
             "justification": "detailed reason for priority",
             "estimated_cost": float,
             "affected_population": int,
             "category": "string"
           }}

        Ensure the justification is data-driven and professional.
        """

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    response_mime_type="application/json",
                )
            )
            
            recommendations_raw = json.loads(response.text)
            
            # Map raw JSON to Domain Models
            recommendations = []
            for rec in recommendations_raw:
                recommendations.append(ProjectRecommendation(
                    **rec,
                    location_cluster=[], # In production, this would be calculated via geospatial clustering
                    supporting_feedback_ids=[] # In production, Gemini would return these IDs
                ))
            
            return recommendations
        except Exception as e:
            logger.error(f"Gemini Analysis Error: {e}")
            return []
