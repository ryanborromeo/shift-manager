from pydantic import BaseModel, field_validator
from zoneinfo import ZoneInfo, available_timezones


class TimezoneSettings(BaseModel):
    timezone: str

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
