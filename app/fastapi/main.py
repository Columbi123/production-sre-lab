
from fastapi import FastAPI

app = FastAPI(
    title="Production SRE Lab API",
    description="Application for SRE infrastructure practice",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "message": "Welcome to Production SRE Lab",
        "status": "running",
        "version": "0.1.0"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "sre-api"
    }
