from fastapi import FastAPI, HTTPException
from pydantic import ValidationError
from app.models import TimezoneSettings
from app.crud import get_timezone_setting, update_timezone_setting

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
