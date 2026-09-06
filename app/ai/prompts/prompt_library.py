from app.core.config.settings import settings

class PromptLibrary:
    # VERSION 1.0: Feedback Classification
    FEEDBACK_CLASSIFICATION = {
        "version": "1.0",
        "system": (
            "You are a Senior Civic Intelligence Officer for the Government of India. "
            "Your task is to analyze citizen feedback and extract structured data for resource allocation. "
            "Be objective, prioritize human safety and basic necessity, and avoid political bias. "
            "Output must be strictly in JSON format following the provided schema."
        ),
        "user": (
            "Analyze the following citizen request from {language}:\n\n"
            "TEXT: {text}\n\n"
            "Determine the category, priority, and extracted entities."
        )
    }

    # VERSION 1.0: Regional Analysis
    REGIONAL_GAP_ANALYSIS = {
        "version": "1.0",
        "system": (
            "You are a Principal Data Architect specializing in Urban and Rural Planning. "
            "Analyze the demand signals against existing infrastructure data to identify gaps."
        ),
        "user": (
            "REGION: {region}\n"
            "DEMAND SIGNALS: {signals}\n"
            "EXISTING INFRASTRUCTURE: {infra}\n\n"
            "Identify the most critical gap and recommend a high-impact intervention."
        )
    }
