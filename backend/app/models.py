from pydantic import BaseModel, Field, field_validator
from zoneinfo import ZoneInfo, available_timezones


class TimezoneSettings(BaseModel):
    timezone: str = Field(
        ...,
        description="IANA timezone name (e.g., 'America/New_York', 'Europe/London')",
        examples=["America/New_York", "Europe/London", "Asia/Tokyo"]
    )

    @field_validator("timezone")
    @classmethod
    def validate_timezone(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Timezone cannot be empty")
        if v not in available_timezones():
            raise ValueError(f"Invalid timezone: {v}")
        try:
            ZoneInfo(v)
        except Exception:
            raise ValueError(f"Invalid timezone: {v}")
        return v


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
