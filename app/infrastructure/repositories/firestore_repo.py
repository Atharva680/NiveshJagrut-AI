from google.cloud import firestore
from typing import List, Optional
from app.domain.models.citizen_request import CitizenRequest
from app.domain.interfaces.citizen_repo import ICitizenRequestRepository
from app.core.config.settings import settings

class FirestoreCitizenRepository(ICitizenRequestRepository):
    def __init__(self):
        self.db = firestore.Client(project=settings.PROJECT_ID)
        self.collection = self.db.collection("citizen_requests")

    async def save(self, request: CitizenRequest) -> str:
        doc_ref = self.collection.document(request.request_id)
        doc_ref.set(request.dict())
        return request.request_id

    async def get_by_id(self, request_id: str) -> Optional[CitizenRequest]:
        doc = self.collection.document(request_id).get()
        if doc.exists:
            return CitizenRequest(**doc.to_dict())
        return None

    async def list_by_region(self, state: str, district: Optional[str] = None) -> List[CitizenRequest]:
        query = self.collection.where("location.state", "==", state)
        if district:
            query = query.where("location.district", "==", district)
        
        docs = query.stream()
        return [CitizenRequest(**doc.to_dict()) for doc in docs]

    async def update_status(self, request_id: str, status: str, metadata: dict = None):
        doc_ref = self.collection.document(request_id)
        update_data = {"status": status}
        if metadata:
            update_data["metadata"] = metadata
        doc_ref.update(update_data)
