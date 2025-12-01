import os
from typing import List
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from app.models import Worker, WorkerCreate, WorkerUpdate, ShiftResponse, ShiftCreate, ShiftUpdate
from app.crud import (
    list_workers, create_worker, get_worker, update_worker, delete_worker,
    list_shifts, create_shift, get_shift, update_shift, delete_shift
)

ENV = os.getenv("ENV", "development")

app = FastAPI(
    title="Shift Manager API",
    version="0.1.0",
    description="API for managing workers and shift scheduling with timezone support",
    docs_url="/docs" if ENV != "production" else None,
    redoc_url="/redoc" if ENV != "production" else None,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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


@app.get(
    "/shifts",
    response_model=List[ShiftResponse],
    tags=["Shifts"],
    summary="List All Shifts",
    description="Retrieves a list of all shifts with times in the current preferred timezone",
    responses={
        200: {
            "description": "List of shifts retrieved successfully",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "worker_id": 1,
                            "start": "2024-02-10T09:00:00-05:00",
                            "end": "2024-02-10T17:00:00-05:00",
                            "duration_hours": 8.0
                        }
                    ]
                }
            },
        },
    },
)
def get_shifts():
    shifts = list_shifts()
    return shifts


@app.post(
    "/shifts",
    response_model=ShiftResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Shifts"],
    summary="Create Shift",
    description="Creates a new shift with timezone-aware timestamps. Validates worker exists, shift doesn't exceed 12 hours, and doesn't overlap with existing shifts.",
    responses={
        201: {
            "description": "Shift created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "worker_id": 1,
                        "start": "2024-02-10T09:00:00-05:00",
                        "end": "2024-02-10T17:00:00-05:00",
                        "duration_hours": 8.0
                    }
                }
            },
        },
        400: {
            "description": "Validation error (worker not found, overlap, or duration exceeded)",
            "content": {
                "application/json": {
                    "example": {"detail": "Worker not found"}
                }
            },
        },
    },
)
def post_shift(shift: ShiftCreate):
    try:
        created = create_shift(shift.worker_id, shift.start, shift.end)
        return created
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get(
    "/shifts/{shift_id}",
    response_model=ShiftResponse,
    tags=["Shifts"],
    summary="Get Shift by ID",
    description="Retrieves a specific shift by its ID with times in the current preferred timezone",
    responses={
        200: {
            "description": "Shift retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "worker_id": 1,
                        "start": "2024-02-10T09:00:00-05:00",
                        "end": "2024-02-10T17:00:00-05:00",
                        "duration_hours": 8.0
                    }
                }
            },
        },
        404: {
            "description": "Shift not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Shift not found"}
                }
            },
        },
    },
)
def get_shift_by_id(shift_id: int):
    shift = get_shift(shift_id)
    if shift is None:
        raise HTTPException(status_code=404, detail="Shift not found")
    return shift


@app.put(
    "/shifts/{shift_id}",
    response_model=ShiftResponse,
    tags=["Shifts"],
    summary="Update Shift",
    description="Updates an existing shift with full shift data. Validates worker exists, shift doesn't exceed 12 hours, and doesn't overlap with other shifts.",
    responses={
        200: {
            "description": "Shift updated successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "worker_id": 1,
                        "start": "2024-02-10T10:00:00-05:00",
                        "end": "2024-02-10T18:00:00-05:00",
                        "duration_hours": 8.0
                    }
                }
            },
        },
        400: {
            "description": "Validation error (worker not found, overlap, or duration exceeded)",
            "content": {
                "application/json": {
                    "example": {"detail": "Shift overlaps with existing shift for this worker"}
                }
            },
        },
        404: {
            "description": "Shift not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Shift not found"}
                }
            },
        },
    },
)
def put_shift(shift_id: int, shift: ShiftUpdate):
    try:
        updated = update_shift(shift_id, shift.worker_id, shift.start, shift.end)
        if updated is None:
            raise HTTPException(status_code=404, detail="Shift not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete(
    "/shifts/{shift_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Shifts"],
    summary="Delete Shift",
    description="Deletes a shift by its ID",
    responses={
        204: {
            "description": "Shift deleted successfully",
        },
        404: {
            "description": "Shift not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Shift not found"}
                }
            },
        },
    },
)
def delete_shift_by_id(shift_id: int):
    result = delete_shift(shift_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Shift not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
