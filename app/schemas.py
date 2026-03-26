from pydantic import BaseModel
from typing import Optional

class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None


class TaskResponse(BaseModel):
    id: int
    owner_id: int
    title: str
    completed: bool

    model_config = {
        "from_attributes": True
    }

class MessageResponse(BaseModel):
    message: str