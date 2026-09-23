from typing import Optional
from pydantic import BaseModel, Field
import uuid
from datetime import datetime

class Milestone(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    task_id: str
    team_id: str
    title: str
    points: int = 25
    status: str = "in_progress"  # in_progress, completed
    completed_at: Optional[str] = None
