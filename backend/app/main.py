from typing import List
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import ValidationError
from app.models import TimezoneSettings, Worker, WorkerCreate, WorkerUpdate
from app.crud import get_timezone_setting, update_timezone_setting, list_workers, create_worker, get_worker, update_worker, delete_worker

app = FastAPI(
    title="Shift Manager API",
    version="0.1.0",
    description="API for managing workers and shift scheduling with timezone support",
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.get(
    "/",
    tags=["General"],
    summary="API Root",
    description="Returns API information and status",
)
def read_root():
    return {
        "message": "Welcome to Shift Manager API",
        "status": "running",
        "version": "0.1.0"
    }


@app.get(
    "/health",
    tags=["General"],
    summary="Health Check",
    description="Returns the health status of the API",
)
def health_check():
    return {"status": "healthy"}


@app.get(
    "/settings/timezone",
    tags=["Settings"],
    summary="Get Timezone Setting",
    description="Retrieves the current timezone setting for the shift manager",
    responses={
        200: {
            "description": "Timezone setting retrieved successfully",
            "content": {
                "application/json": {
                    "example": {"timezone": "America/New_York"}
                }
            },
        },
    },
)
def get_timezone():
    timezone = get_timezone_setting()
    return {"timezone": timezone}


@app.put(
    "/settings/timezone",
    tags=["Settings"],
    summary="Update Timezone Setting",
    description="Updates the timezone setting for the shift manager. Accepts IANA timezone names (e.g., 'America/New_York', 'Europe/London')",
    responses={
        200: {
            "description": "Timezone setting updated successfully",
            "content": {
                "application/json": {
                    "example": {"timezone": "America/New_York"}
                }
            },
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {"detail": "Error updating timezone"}
                }
            },
        },
    },
)
def put_timezone(settings: TimezoneSettings):
    try:
        timezone = update_timezone_setting(settings.timezone)
        return {"timezone": timezone}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/workers",
    response_model=List[Worker],
    tags=["Workers"],
    summary="List All Workers",
    description="Retrieves a list of all registered workers",
    responses={
        200: {
            "description": "List of workers retrieved successfully",
            "content": {
                "application/json": {
                    "example": [
                        {"id": 1, "name": "John Doe"},
                        {"id": 2, "name": "Jane Smith"}
                    ]
                }
            },
        },
    },
)
def get_workers():
    workers = list_workers()
    return workers


@app.post(
    "/workers",
    response_model=Worker,
    status_code=status.HTTP_201_CREATED,
    tags=["Workers"],
    summary="Create Worker",
    description="Creates a new worker with the provided name",
    responses={
        201: {
            "description": "Worker created successfully",
            "content": {
                "application/json": {
                    "example": {"id": 1, "name": "John Doe"}
                }
            },
        },
    },
)
def post_worker(worker: WorkerCreate):
    created = create_worker(worker.name)
    return created


@app.get(
    "/workers/{worker_id}",
    response_model=Worker,
    tags=["Workers"],
    summary="Get Worker by ID",
    description="Retrieves a specific worker by their ID",
    responses={
        200: {
            "description": "Worker retrieved successfully",
            "content": {
                "application/json": {
                    "example": {"id": 1, "name": "John Doe"}
                }
            },
        },
        404: {
            "description": "Worker not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Worker not found"}
                }
            },
        },
    },
)
def get_worker_by_id(worker_id: int):
    worker = get_worker(worker_id)
    if worker is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    return worker


@app.put(
    "/workers/{worker_id}",
    response_model=Worker,
    tags=["Workers"],
    summary="Update Worker",
    description="Updates an existing worker's information",
    responses={
        200: {
            "description": "Worker updated successfully",
            "content": {
                "application/json": {
                    "example": {"id": 1, "name": "John Doe Updated"}
                }
            },
        },
        404: {
            "description": "Worker not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Worker not found"}
                }
            },
        },
    },
)
def put_worker(worker_id: int, worker: WorkerUpdate):
    updated = update_worker(worker_id, worker.name)
    if updated is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    return updated


@app.delete(
    "/workers/{worker_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Workers"],
    summary="Delete Worker",
    description="Deletes a worker by their ID",
    responses={
        204: {
            "description": "Worker deleted successfully",
        },
        404: {
            "description": "Worker not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Worker not found"}
                }
            },
        },
    },
)
def delete_worker_by_id(worker_id: int):
    result = delete_worker(worker_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
