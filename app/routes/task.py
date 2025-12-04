from fastapi import APIRouter, HTTPException, Query
from datetime import datetime, timezone
from models.schemas import TaskCreate, TaskResponse, TaskStatus
from typing import Optional, Literal
from core.database import tasks_db
import uuid

router = APIRouter()

@router.post("/tasks", response_model=TaskResponse, status_code=201)
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

@router.get("/tasks")
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
        filtered = [i for i in filtered if i["status"] == status]
        
    if search:
        key = search.lower()
        filtered = [i for i in filtered if key in i["title"].lower() or key in i["description"].lower()]
        
    if created_from:
        filtered = [i for i in filtered if i["created_at"] >= created_from]
        
    if created_to:
        filtered = [i for i in filtered if i["created_at"] <= created_to]
        
    if updated_from:
        filtered = [i for i in filtered if i["updated_at"] >= updated_from]
        
    if updated_to:
        filtered = [i for i in filtered if i["updated_at"] <= updated_to]
        
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