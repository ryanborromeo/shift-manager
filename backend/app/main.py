from fastapi import FastAPI

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
