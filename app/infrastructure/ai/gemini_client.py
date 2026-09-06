
import google.generativeai as genai
from app.core.config.settings import settings
from app.ai.prompts.prompt_library import PromptLibrary
from app.ai.schemas.classification import RequestClassification
import json
import logging

logger = logging.getLogger(__name__)

class GeminiAIClient:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        # Deterministic text model for classification
        self.text_model = genai.GenerativeModel(
            model_name=settings.GEMINI_MODEL,
            generation_config={"temperature": 0.1, "response_mime_type": "application/json"}
        )
        # Flash model for fast multimodal vision analysis
        self.vision_model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    def classify_request(self, text: str, language: str) -> RequestClassification:
        prompt_cfg = PromptLibrary.FEEDBACK_CLASSIFICATION
        user_prompt = prompt_cfg["user"].format(language=language, text=text)
        try:
            response = self.text_model.generate_content([prompt_cfg["system"], user_prompt])
            return RequestClassification(**json.loads(response.text))
        except Exception as e:
            logger.error(f"AI Classification failed: {str(e)}")
            raise RuntimeError(f"AI Classification Error: {str(e)}")

    def analyze_infrastructure_image(self, image_bytes: bytes, context_text: str) -> dict:
        """
        Verifies a citizen's claim using a photo.
        Returns structured data about the damage.
        """
        prompt = (
            f"You are a Civil Engineering Inspector. Analyze this image in the context of: '{context_text}'. "
            "Identify if the image shows actual infrastructure failure. "
            "Return JSON with: { 'verified': bool, 'severity': 1-10, 'observations': str, 'confidence': 0-1 }"
        )
        try:
            response = self.vision_model.generate_content([
                prompt, 
                {"mime_type": "image/jpeg", "data": image_bytes}
            ])
            # Use a simple JSON extraction if the model doesn't use mime_type for flash
            return json.loads(response.text.replace('```json', '').replace('```', ''))
        except Exception as e:
            logger.error(f"Vision Analysis failed: {str(e)}")
            return {"verified": False, "error": str(e)}

    def generate_policy_recommendation(self, analysis_report: dict) -> str:
        """
        The 'Policymaker' Tool. Converts raw gap analysis into a strategic proposal.
        """
        prompt = (
            f"ACT AS: Principal Urban Planner & Government Advisor.\n"
            f"ANALYSIS REPORT: {json.dumps(analysis_report)}\n\n"
            "TASK: Generate a professional Investment Recommendation. "
            "Include: Project Title, Strategic Justification, Estimated Budget Category, "
            "Expected Citizen Impact, and Implementation Timeline."
        )
        response = self.text_model.generate_content(prompt)
        return response.text
