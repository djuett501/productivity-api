from fastapi import FastAPI
from app.routers.tasks import router as task_manager

app = FastAPI()

app.include_router(task_manager)