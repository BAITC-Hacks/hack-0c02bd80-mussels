from pydantic import BaseModel, Field
import uuid
from datetime import datetime

class Proposal(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    task_id: str
    team_id: str
    team_name: str
    solution_idea: str
    plan: str
    timeline: str
    prototype_url: str = ""
    status: str = "pending"  # pending, accepted, rejected
    submitted_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    review_comment: str = ""
