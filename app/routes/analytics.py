from fastapi import APIRouter
from datetime import datetime, timezone, timedelta
from models.schemas import TaskStatus
from core.database import tasks_db
import pandas as pd

router = APIRouter()

@router.get("/summary")
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
