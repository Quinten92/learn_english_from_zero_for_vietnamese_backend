from fastapi import FastAPI
from .routers import items

app = FastAPI()

app.include_router(items.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Learn English API"}
