from pydantic import BaseModel, Field
from typing import List, Optional

class RequestClassification(BaseModel):
    category: str = Field(..., description="The broad category of the request (e.g., Water, Road, Education)")
    sub_category: str = Field(..., description="Specific type of issue (e.g., Leakage, Potholes, Lack of Teachers)")
    priority: str = Field(..., description="Critical, High, Medium, or Low based on urgency and impact")
    urgency_rationale: str = Field(..., description="Reasoning for the assigned priority")
    entities: List[str] = Field(default=[], description="Key locations or assets mentioned")
    sentiment: str = Field(..., description="Tone of the request (e.g., frustrated, urgent, hopeful)")
