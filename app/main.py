from fastapi import FastAPI
from app.routers.tasks import router as task_manager
from app.routers.auth import router as authorization
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.database import engine, Base
from app import models

app = FastAPI()

app.include_router(task_manager)
app.include_router(authorization)

@app.get("/db-test")
def db_test(db: Session = Depends(get_db)):
    return {"status": "connected"}


Base.metadata.create_all(bind=engine)