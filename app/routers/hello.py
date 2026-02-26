from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.get("/hello")
def say_hello():
    return {"message" : "Hello, how are you?"}

@router.get("/hello/{name}")
def say_hello_name(name: str):
    return {"message": f"Hello, {name}"}

