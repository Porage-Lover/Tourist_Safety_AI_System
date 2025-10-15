from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel
import logging
from processing.data_pipeline import run_full_pipeline
from typing import Dict

router = APIRouter()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

job_statuses: Dict[str, str] = {}

class PipelineTriggerResponse(BaseModel):
    job_id: str
    status: str
    message: str

class JobStatusResponse(BaseModel):
    job_id: str
    status: str

def run_pipeline_background(job_id: str):
    try:
        logger.info(f"Starting data ingestion pipeline for job_id: {job_id}")
        job_statuses[job_id] = "running"
        run_full_pipeline()
        job_statuses[job_id] = "completed"
        logger.info(f"Data ingestion pipeline for job_id: {job_id} completed.")
    except Exception as e:
        logger.error(f"Error during data ingestion pipeline for job_id: {job_id}. Error: {e}", exc_info=True)
        job_statuses[job_id] = "failed"

@router.post("/ingestion/trigger-pipeline", response_model=PipelineTriggerResponse)
async def trigger_pipeline(background_tasks: BackgroundTasks):
    job_id = f"pipeline_{len(job_statuses) + 1}"
    job_statuses[job_id] = "queued"
    background_tasks.add_task(run_pipeline_background, job_id)
    return {"job_id": job_id, "status": "queued", "message": "Data ingestion pipeline has been initiated."}

@router.get("/ingestion/status/{job_id}", response_model=JobStatusResponse)
async def get_pipeline_status(job_id: str):
    status = job_statuses.get(job_id)
    if not status:
        raise HTTPException(status_code=404, detail="Job ID not found.")
    return {"job_id": job_id, "status": status}
