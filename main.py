import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from services.geospatial_risk import router as geospatial_router
from services.behavioral_anomaly import router as behavioral_router
from services.predictive_alert import router as predictive_router
from services.data_ingestion import router as ingestion_router
from core.config import settings
from core.lifespan import startup_events, shutdown_events

# Lifespan manager to handle startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup and shutdown events.
    """
    print("AI Service is starting up...")
    await startup_events()
    yield
    print("AI Service is shutting down...")
    await shutdown_events()

# Initialize the main FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# --- API Router Inclusion ---
print("Including API routers...")
app.include_router(ingestion_router, prefix=settings.API_V1_STR, tags=["Data Ingestion"])
app.include_router(geospatial_router, prefix=settings.API_V1_STR, tags=["Geospatial Risk"])
app.include_router(behavioral_router, prefix=settings.API_V1_STR, tags=["Behavioral Anomaly"])
app.include_router(predictive_router, prefix=settings.API_V1_STR, tags=["Predictive Alerts"])

# --- Root Endpoint ---
@app.get("/", tags=["Root"])
async def read_root():
    """
    Root GET endpoint. Provides a welcome message and basic API information.
    """
    return {
        "message": "Welcome to the Tourist Safety AI System API",
        "documentation": "/docs",
        "project": settings.PROJECT_NAME
    }

# --- Main Execution Block ---
if __name__ == "__main__":
    print(f"Starting server at http://{settings.SERVER_HOST}:{settings.SERVER_PORT}")
    uvicorn.run(
        "main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=True
    )
