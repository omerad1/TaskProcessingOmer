from fastapi import FastAPI
from app.routers import tasks
from app.services.sqlite_service import init_db

init_db()  # Ensures the database is initialized when the app starts

app = FastAPI(
    title="Welcome to Task Processing Omer",
    version="1.0.0"
)

app.include_router(tasks.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI API with SQLite!"}
