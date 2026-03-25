from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from dataclasses import dataclass
from typing import Any
from datetime import datetime, timezone
from app.stubs import get_current_user, User
from app.proto_db import TASKS
from typing import Optional

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)

class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None

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

@router.post("")
def create_task(task_data: TaskCreate, current_user: User = Depends(get_current_user)):
    new_id = max(task["id"] for task in TASKS)+1

    new_task = {
        "id": new_id,
        "owner_id": current_user.id,
        "title": task_data.title,
        "completed": False
    }

    TASKS.append(new_task)

    return {"task": new_task}

@router.delete("/{task_id}")
def remove_task(task_id: int, current_user: User = Depends(get_current_user)):
    for task in TASKS:
        if task["id"] == task_id and task["owner_id"] == current_user.id:
            TASKS.remove(task)
            return {"message": "Task deleted"}
        
    ##if task was not found during iteration, 404 error
    raise HTTPException(status_code=404, detail="Task not found")

@router.patch("/{task_id}")
def update_task(task_id: int, update_data: TaskUpdate, current_user = Depends(get_current_user)):
    for task in TASKS:
        if task["id"] == task_id and task["owner_id"] == current_user.id:
            task.update(update_data.dict(exclude_unset=True))
            return
        
    raise HTTPException(status_code=404, detail="Task not found")