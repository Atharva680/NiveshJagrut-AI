from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum

class FeedbackChannel(str, Enum):
    VOICE = "voice"
    TEXT = "text"
    WHATSAPP = "whatsapp"
    SMS = "sms"

class FeedbackStatus(str, Enum):
    RECEIVED = "received"
    PROCESSED = "processed"
    ANALYZED = "analyzed"
    ACTIONED = "actioned"

class CitizenFeedback(BaseModel):
    id: Optional[str] = None
    citizen_id: str
    language: str
    original_content: str
    translated_content: Optional[str] = None
    channel: FeedbackChannel
    location: Dict[str, float] = Field(..., description="{'lat': 0.0, 'lng': 0.0}")
    pincode: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    status: FeedbackStatus = FeedbackStatus.RECEIVED
    category: Optional[str] = None

class InfrastructureData(BaseModel):
    region_id: str
    infrastructure_type: str # e.g., "Roads", "Water", "Electricity"
    current_status: str # e.g., "Critical", "Degraded", "Good"
    last_updated: datetime
    budget_allocated: float

class ProjectRecommendation(BaseModel):
    project_id: str
    title: str
    priority_score: float = Field(..., ge=0, le=100)
    justification: str
    estimated_cost: float
    affected_population: int
    location_cluster: List[Dict[str, float]]
    supporting_feedback_ids: List[str]
    category: str
