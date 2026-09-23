from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import uuid
from datetime import datetime

class TaskDraft(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    raw_text: str
    industry: str = "Ритейл и e-commerce"
    task_type: str = "Диалоговый AI и чат-боты"
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())

class TaskCard(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    title: str
    industry: str
    task_type: str
    context_need: str = ""
    data_materials: str = ""
    expected_result: str = ""
    success_criteria: str = ""
    constraints: str = ""
    target_users: str = ""
    business_contact: str = ""
    rating: int = 0
    readiness_level: str = "Черновик"
    rating_breakdown: Dict[str, int] = Field(default_factory=dict)
    missing_fields: List[str] = Field(default_factory=list)
    published: bool = True
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now().isoformat())
