from typing import List
from pydantic import BaseModel, Field
import uuid

class StudentTeam(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str
    industry_interests: List[str] = Field(default_factory=list)
    task_type_interests: List[str] = Field(default_factory=list)
    skills: List[str] = Field(default_factory=list)
    preferred_readiness: str = "Любая"
    progress_points: int = 0
    completed_milestones: List[str] = Field(default_factory=list)
