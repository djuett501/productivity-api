from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False, index=True)
    completed = Column(Boolean, default=False)


