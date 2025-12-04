from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from enum import Enum
from datetime import datetime, timedelta, timezone
import pandas as pd
import uuid

app = FastAPI()

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

tasks_db: List[dict] = []

@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(payload: TaskCreate):
    now = datetime.now(timezone.utc)
    task = {
        "id": str(uuid.uuid4()),
        "title": payload.title,
        "description": payload.description,
        "status": payload.status,
        "created_at": now,
        "updated_at": now
    }
    
    tasks_db.append(task)
    return task

@app.get("/tasks")
def list_tasks(status: Optional[TaskStatus] = None,
    search: Optional[str] = None,
    created_from: Optional[datetime] = None,
    created_to: Optional[datetime] = None,
    updated_from: Optional[datetime] = None,
    updated_to: Optional[datetime] = None,
    sort_by: str = Query(default="created_at"),
    order: Literal["asc", "desc"] = Query(default="asc"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100)):
    
    valid_sort_fields = ["id", "title", "description", "status", "created_at", "updated_at"]
    
    if sort_by not in valid_sort_fields:
        raise HTTPException(status_code=400, detail="Invalid sort field")
    
    filtered = tasks_db.copy()
    
    if status:
        filtered = [t for t in filtered if t["status"] == status]
        
    if search:
        key = search.lower()
        filtered = [t for t in filtered if key in t["title"].lower() or key in t["description"].lower()]
        
    if created_from:
        filtered = [t for t in filtered if t["created_at"] >= created_from]
        
    if created_to:
        filtered = [t for t in filtered if t["created_at"] <= created_to]
        
    if updated_from:
        filtered = [t for t in filtered if t["updated_at"] >= updated_from]
        
    if updated_to:
        filtered = [t for t in filtered if t["updated_at"] <= updated_to]
        
    reverse = order == "desc"
    filtered.sort(key=lambda x: x[sort_by], reverse=reverse)
    total = len(filtered)
    start = (page - 1) * page_size
    end = start + page_size
    items = filtered[start:end]
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": items
    }

@app.get("/analytics/summary")
def get_analytics():
    if not tasks_db:
        
        return {
            "status_distribution": {},
            "weekly_completion_rate": 0.0,
            "avg_daily_tasks": 0.0
        }
        
    df = pd.DataFrame(tasks_db)
    status_distribution = df["status"].value_counts().to_dict()
    now = datetime.now(timezone.utc)
    week_ago = now - timedelta(days=7)
    recent = df[df["created_at"] >= week_ago]
    
    if recent.empty:
        weekly_completion_rate = 0.0
    else:
        completed_recent = recent[recent["status"] == TaskStatus.completed]
        weekly_completion_rate = len(completed_recent) / len(recent)
        
    df["created_date"] = pd.to_datetime(df["created_at"]).dt.date
    daily_counts = df.groupby("created_date")["id"].count()
    avg_daily_tasks = float(daily_counts.mean()) if not daily_counts.empty else 0.0
    
    return {
        "status_distribution": status_distribution,
        "weekly_completion_rate": weekly_completion_rate,
        "avg_daily_tasks": avg_daily_tasks
    }
