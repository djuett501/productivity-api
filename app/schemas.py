from pydantic import BaseModel, EmailStr, Field
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

    