from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator, computed_field


class Worker(BaseModel):
    id: int = Field(..., description="Unique identifier for the worker", examples=[1])
    name: str = Field(..., description="Worker's full name", examples=["John Doe"])


class WorkerCreate(BaseModel):
    name: str = Field(
        ...,
        description="Worker's full name",
        examples=["John Doe", "Jane Smith"]
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Name cannot be empty")
        return v


class WorkerUpdate(BaseModel):
    name: str = Field(
        ...,
        description="Updated worker's full name",
        examples=["John Doe Updated", "Jane Smith Updated"]
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Name cannot be empty")
        return v


class Shift(BaseModel):
    id: int = Field(..., description="Unique identifier for the shift", examples=[1])
    worker_id: int = Field(..., description="ID of the worker assigned to this shift", examples=[1])
    start: str = Field(
        ...,
        description="Shift start time in ISO 8601 format with timezone",
        examples=["2024-02-10T09:00:00-05:00"]
    )
    end: str = Field(
        ...,
        description="Shift end time in ISO 8601 format with timezone",
        examples=["2024-02-10T17:00:00-05:00"]
    )


class ShiftCreate(BaseModel):
    worker_id: int = Field(..., description="ID of the worker assigned to this shift", examples=[1])
    start: str = Field(
        ...,
        description="Shift start time in ISO 8601 format with timezone",
        examples=["2024-02-10T09:00:00-05:00"]
    )
    end: str = Field(
        ...,
        description="Shift end time in ISO 8601 format with timezone",
        examples=["2024-02-10T17:00:00-05:00"]
    )

    @field_validator("start", "end")
    @classmethod
    def validate_datetime(cls, v: str) -> str:
        try:
            datetime.fromisoformat(v)
        except ValueError:
            raise ValueError(f"Invalid ISO 8601 datetime format: {v}")
        return v

    @field_validator("end")
    @classmethod
    def validate_end_after_start(cls, v: str, info) -> str:
        if "start" in info.data:
            start_dt = datetime.fromisoformat(info.data["start"])
            end_dt = datetime.fromisoformat(v)
            if end_dt <= start_dt:
                raise ValueError("End time must be after start time")
            
            duration_hours = (end_dt - start_dt).total_seconds() / 3600
            if duration_hours > 12.0:
                raise ValueError("Shift duration cannot exceed 12 hours")
        return v


class ShiftUpdate(BaseModel):
    worker_id: int = Field(..., description="ID of the worker assigned to this shift", examples=[1])
    start: str = Field(
        ...,
        description="Shift start time in ISO 8601 format with timezone",
        examples=["2024-02-10T09:00:00-05:00"]
    )
    end: str = Field(
        ...,
        description="Shift end time in ISO 8601 format with timezone",
        examples=["2024-02-10T17:00:00-05:00"]
    )

    @field_validator("start", "end")
    @classmethod
    def validate_datetime(cls, v: str) -> str:
        try:
            datetime.fromisoformat(v)
        except ValueError:
            raise ValueError(f"Invalid ISO 8601 datetime format: {v}")
        return v

    @field_validator("end")
    @classmethod
    def validate_end_after_start(cls, v: str, info) -> str:
        if "start" in info.data:
            start_dt = datetime.fromisoformat(info.data["start"])
            end_dt = datetime.fromisoformat(v)
            if end_dt <= start_dt:
                raise ValueError("End time must be after start time")
            
            duration_hours = (end_dt - start_dt).total_seconds() / 3600
            if duration_hours > 12.0:
                raise ValueError("Shift duration cannot exceed 12 hours")
        return v


class ShiftResponse(BaseModel):
    id: int = Field(..., description="Unique identifier for the shift", examples=[1])
    worker_id: int = Field(..., description="ID of the worker assigned to this shift", examples=[1])
    start: str = Field(
        ...,
        description="Shift start time in ISO 8601 format with timezone",
        examples=["2024-02-10T09:00:00-05:00"]
    )
    end: str = Field(
        ...,
        description="Shift end time in ISO 8601 format with timezone",
        examples=["2024-02-10T17:00:00-05:00"]
    )
    
    @computed_field
    @property
    def duration_hours(self) -> float:
        start_dt = datetime.fromisoformat(self.start)
        end_dt = datetime.fromisoformat(self.end)
        return (end_dt - start_dt).total_seconds() / 3600


# Timezone related models
class TimezoneOffset(BaseModel):
    seconds: int = Field(..., description="Offset from UTC in seconds", examples=[3600])
    milliseconds: int = Field(..., description="Offset from UTC in milliseconds", examples=[3600000])


class TimezoneInfo(BaseModel):
    timezone: str = Field(..., description="IANA timezone identifier", examples=["America/New_York"])
    currentLocalTime: str = Field(..., description="Current local time in ISO 8601 format", examples=["2024-02-10T14:30:00"])
    currentUtcOffset: TimezoneOffset = Field(..., description="Current UTC offset")
    standardUtcOffset: TimezoneOffset = Field(..., description="Standard (non-DST) UTC offset")
    hasDayLightSaving: bool = Field(..., description="Whether the timezone observes DST")
    isDayLightSavingActive: bool = Field(..., description="Whether DST is currently active")


class TimezoneUpdate(BaseModel):
    timezone: str = Field(..., description="IANA timezone identifier to set", examples=["America/New_York"])


class AvailableTimezonesResponse(BaseModel):
    timezones: List[str] = Field(..., description="List of available IANA timezone identifiers")
