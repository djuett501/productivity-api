from fastapi import APIRouter, Depends, HTTPException
from dataclasses import dataclass
from typing import Any
from datetime import datetime, timezone
from app.stubs import get_current_user, User
from app.proto_db import TASKS

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)

@router.get("")
def show_tasks(current_user: User = Depends(get_current_user)):
    user_tasks = [task for task in TASKS if task["owner_id"] == current_user.id]

    return {
        "owner_id": current_user.id,
        "tasks": user_tasks
    }

@router.get("/{task_id}")
def show_task_id(task_id: int, current_user: User = Depends(get_current_user)):
    for task in TASKS: 
        if task["id"] == task_id and task["owner_id"] == current_user.id:
            return {"task": task}
    raise HTTPException(status_code=404, detail="Task not found")