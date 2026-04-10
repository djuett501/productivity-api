from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc

from app.auth import get_current_user
from app.database import get_db
from app.models import Task, User
from app.schemas import TaskCreate, TaskUpdate, TaskResponse, MessageResponse

from datetime import date
from typing import Literal, Optional

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)

@router.get("", response_model=list[TaskResponse])
def show_tasks(
    completed: Optional[bool] = None,
    due_date: Optional[date] = None,
    priority: Optional[int] = Query(None, ge=1, le=3),
    sort_by: Optional[Literal["due_date", "priority", "completed"]] = None,
    sort_order: Literal["asc", "desc"] = "asc",
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    query = db.query(Task).filter(Task.owner_id == current_user.id)

    if completed is not None:
        query = query.filter(Task.completed == completed)
    
    if due_date is not None:
        query = query.filter(Task.due_date == due_date)

    if priority is not None:
        query = query.filter(Task.priority == priority)

    if sort_by:
        sort_column = getattr(Task, sort_by)
        if sort_order == "desc":
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))

    return query.all()

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
        
    task: Task = db.query(Task).filter(Task.owner_id == current_user.id, Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task

@router.post("", response_model=TaskResponse)
def create_task(task_data: TaskCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    new_task = Task(
        owner_id=current_user.id,
        title=task_data.title,
        completed=False,
        description=task_data.description,
        priority=task_data.priority,
        due_date=task_data.due_date
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

@router.delete("/{task_id}", response_model=MessageResponse)
def remove_task(task_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
        
    task = db.query(Task).filter(Task.owner_id == current_user.id, Task.id == task_id).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()

    return {"message": "Task deleted"}

@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, update_data: TaskUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    task: Task = db.query(Task).filter(Task.owner_id == current_user.id, Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    data = update_data.model_dump(exclude_unset=True)

    if not data:
        raise HTTPException(status_code=400, detail="No data was provided for update")

    for key, value in data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return task
