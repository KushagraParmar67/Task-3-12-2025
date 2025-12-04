from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field("", max_length=1000)
    status: TaskStatus = TaskStatus.pending

class TaskResponse(BaseModel):
    id: str
    title: str
    description: str
    status: TaskStatus
    created_at: datetime
    updated_at: datetime