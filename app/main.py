from fastapi import FastAPI
from app.routers.tasks import router as task_manager
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.database import engine
from app.models import Base

app = FastAPI()

app.include_router(task_manager)

@app.get("/db-test")
def db_test(db: Session = Depends(get_db)):
    return {"status": "connected"}


Base.metadata.create_all(bind=engine)