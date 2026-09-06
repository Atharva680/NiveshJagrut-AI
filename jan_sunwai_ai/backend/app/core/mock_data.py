from app.models.domain import InfrastructureData
from datetime import datetime
from typing import List

class MockDataGenerator:
    @staticmethod
    def get_sample_infrastructure() -> List[InfrastructureData]:
        return [
            InfrastructureData(
                region_id="DELHI_SOUTH",
                infrastructure_type="Roads",
                current_status="Critical",
                last_updated=datetime.utcnow(),
                budget_allocated=5000000.0
            ),
            InfrastructureData(
                region_id="DELHI_SOUTH",
                infrastructure_type="Water",
                current_status="Degraded",
                last_updated=datetime.utcnow(),
                budget_allocated=2000000.0
            ),
            InfrastructureData(
                region_id="BENGALURU_EAST",
                infrastructure_type="Roads",
                current_status="Critical",
                last_updated=datetime.utcnow(),
                budget_allocated=10000000.0
            ),
            InfrastructureData(
                region_id="MUMBAI_WEST",
                infrastructure_type="Electricity",
                current_status="Good",
                last_updated=datetime.utcnow(),
                budget_allocated=1000000.0
            ),
        ]
