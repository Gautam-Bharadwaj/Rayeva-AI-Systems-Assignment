from fastapi import FastAPI
from dotenv import load_dotenv
import os

from app.api.endpoints import router as ai_router

# Load environment variables first
load_dotenv()

app = FastAPI(
    title="Rayeva AI Systems API",
    description="Applied AI modules for Sustainable Commerce",
    version="1.0.0"
)

app.include_router(ai_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "Welcome to Rayeva APIs. Check /docs for endpoints.",
        "environment": os.getenv("ENVIRONMENT", "development")
    }
