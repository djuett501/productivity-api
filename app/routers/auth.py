from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas import UserCreate, UserResponse, UserLogin, TokenResponse
from app.models import User
from app.database import get_db
from app.auth import hash_password, verify_password, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

@router.post("/register", response_model=UserResponse)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    user_exists = db.query(User).filter(User.email == user_data.email).first()

    if user_exists:
        raise HTTPException(status_code=400, detail="Email has already been registered")
    
    new_user = User(
        email = user_data.email,
        hashed_password = hash_password(user_data.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login", response_model=TokenResponse)
def login_user(user_data: UserLogin, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()

    if not existing_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    verified = verify_password(user_data.password, existing_user.hashed_password)
    
    if not verified:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": str(existing_user.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

