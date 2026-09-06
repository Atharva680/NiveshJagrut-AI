from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional, Dict
from enum import Enum

class RequestStatus(str, Enum):
    RECEIVED = "received"
    PROCESSED = "processed"
    ANALYZED = "analyzed"
    ACTIONED = "actioned"
    FAILED = "failed"

class PriorityLevel(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class GeoLocation(BaseModel):
    latitude: float
    longitude: float
    address: Optional[str] = None
    village: Optional[str] = None
    district: Optional[str] = None
    state: str

class CitizenRequest(BaseModel):
    request_id: str
    citizen_id: Optional[str] = None
    original_text: str
    original_language: str
    translated_text: Optional[str] = None
    category: Optional[str] = None
    sub_category: Optional[str] = None
    priority: Optional[PriorityLevel] = None
    location: GeoLocation
    status: RequestStatus = RequestStatus.RECEIVED
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict = {}

class DemandAnalysis(BaseModel):
    region_id: str
    demand_score: float = Field(..., description="Normalized score 0-1")
    primary_needs: List[str]
    infrastructure_gap: str
    affected_population_estimate: int
    urgency_rationale: str
    recommended_action: str
    confidence_score: float
