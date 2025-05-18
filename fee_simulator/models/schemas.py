from pydantic import BaseModel
from typing import List

class FeeScenario(BaseModel):
    participant_type: str
    volume_tier: str
    order_type: str
    estimated_fee: str
    rebate: str
    notes: str

class FeeScenarioAnalysis(BaseModel):
    scenarios: List[FeeScenario] 