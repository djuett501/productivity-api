from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime, date

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[date] = None
    priority: int = Field(default=1, ge=1, le=3)


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None
    due_date: Optional[date] = None
    priority: Optional[int] = Field(default=1, ge=1, le=3)
    description: Optional[str] = None

class TaskResponse(BaseModel):
    id: int
    owner_id: int
    title: str
    completed: bool
    description: Optional[str] = None
    due_date: Optional[date] = None
    priority: int

    model_config = {
        "from_attributes": True
    }

class MessageResponse(BaseModel):
    message: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)

class UserResponse(BaseModel):
    id: int
    email: EmailStr

    model_config = {
        "from_attributes": True
    }

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

    