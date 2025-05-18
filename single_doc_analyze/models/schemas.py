from pydantic import BaseModel
from typing import List

class DocumentAnalysis(BaseModel):
    summary: str
    key_topics: List[str]
    risks_or_issues: List[str]
    recommended_actions: List[str]

class EvaluationResult(BaseModel):
    is_acceptable: bool
    feedback: str 