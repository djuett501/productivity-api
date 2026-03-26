from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.stubs import get_current_user, User
from app.database import get_db
from app.models import Task
from app.schemas import TaskCreate, TaskUpdate, TaskResponse, MessageResponse

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)

@router.get("", response_model=list[TaskResponse])
def show_tasks(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_tasks = db.query(Task).filter(Task.owner_id == current_user.id).all()

    return user_tasks

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
        completed=False
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
