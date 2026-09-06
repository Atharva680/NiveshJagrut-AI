from abc import ABC, abstractmethod
from app.domain.models.citizen_request import CitizenRequest
from typing import Optional, List

class ICitizenRequestRepository(ABC):
    @abstractmethod
    async def save(self, request: CitizenRequest) -> str:
        pass

    @abstractmethod
    async def get_by_id(self, request_id: str) -> Optional[CitizenRequest]:
        pass

    @abstractmethod
    async def list_by_region(self, state: str, district: Optional[str] = None) -> List[CitizenRequest]:
        pass

    @abstractmethod
    async def update_status(self, request_id: str, status: str, metadata: dict = None):
        pass
