from typing import List
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import ValidationError
from app.models import TimezoneSettings, Worker, WorkerCreate, WorkerUpdate
from app.crud import get_timezone_setting, update_timezone_setting, list_workers, create_worker, get_worker, update_worker, delete_worker

app = FastAPI(title="Shift Manager API")


@app.get("/")
def read_root():
    return {
        "message": "Welcome to Shift Manager API",
        "status": "running",
        "version": "0.1.0"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/settings/timezone")
def get_timezone():
    timezone = get_timezone_setting()
    return {"timezone": timezone}


@app.put("/settings/timezone")
def put_timezone(settings: TimezoneSettings):
    try:
        timezone = update_timezone_setting(settings.timezone)
        return {"timezone": timezone}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/workers", response_model=List[Worker])
def get_workers():
    workers = list_workers()
    return workers


@app.post("/workers", response_model=Worker, status_code=status.HTTP_201_CREATED)
def post_worker(worker: WorkerCreate):
    created = create_worker(worker.name)
    return created


@app.get("/workers/{worker_id}", response_model=Worker)
def get_worker_by_id(worker_id: int):
    worker = get_worker(worker_id)
    if worker is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    return worker


@app.put("/workers/{worker_id}", response_model=Worker)
def put_worker(worker_id: int, worker: WorkerUpdate):
    updated = update_worker(worker_id, worker.name)
    if updated is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    return updated


@app.delete("/workers/{worker_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_worker_by_id(worker_id: int):
    result = delete_worker(worker_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
