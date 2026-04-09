from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey,CheckConstraint, Date
from app.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False, index=True)
    completed = Column(Boolean, default=False)
    description = Column(String, nullable=True)
    due_date = Column(Date, nullable=True)
    priority = Column(Integer, nullable=False, default=1)   ## Priority 1 is low, 2 is medium, 3 is high/urgent

    __table_args__ = (
        CheckConstraint("priority >= 1 AND priority <= 3", name="check_priority_range"),
    )    

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
