from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import List, Dict, Any
import random
import time
import uuid
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class GPSPoint(BaseModel):
    latitude: float
    longitude: float
    timestamp: int
    speed: float

class TrailAnalysisRequest(BaseModel):
    tourist_id: str
    trail: List[GPSPoint] = Field(..., min_items=5)

class AnomalyResponse(BaseModel):
    tourist_id: str
    anomaly_score: float
    anomaly_type: str
    is_alert: bool

class JobSubmissionResponse(BaseModel):
    job_id: str
    status_url: str

class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    result: AnomalyResponse | None = None

async_jobs: Dict[str, Any] = {}

def analyze_trail_mock(trail: List[GPSPoint]) -> tuple[float, str, bool]:
    if len(trail) > 10 and all(p.speed < 0.1 for p in trail[-10:]):
        return random.uniform(0.8, 0.98), "Unusual_Immobility", True
    if any(p.speed > 30 for p in trail):
        return random.uniform(0.7, 0.9), "Implausible_Speed", True
    return random.uniform(0.01, 0.25), "Normal", False

def process_long_trail_analysis(job_id: str, trail_request: TrailAnalysisRequest):
    logger.info(f"Starting async analysis for job_id: {job_id}")
    time.sleep(15)
    score, anomaly_type, is_alert = analyze_trail_mock(trail_request.trail)
    result = AnomalyResponse(
        tourist_id=trail_request.tourist_id,
        anomaly_score=round(score, 4),
        anomaly_type=anomaly_type,
        is_alert=is_alert
    )
    async_jobs[job_id] = {"status": "completed", "result": result}
    logger.info(f"Completed async analysis for job_id: {job_id}")

@router.post("/gps-trail/analyze", response_model=AnomalyResponse)
async def analyze_gps_trail(request: TrailAnalysisRequest):
    logger.info(f"Received real-time trail analysis for tourist: {request.tourist_id}")
    score, anomaly_type, is_alert = analyze_trail_mock(request.trail)
    return AnomalyResponse(
        tourist_id=request.tourist_id,
        anomaly_score=round(score, 4),
        anomaly_type=anomaly_type,
        is_alert=is_alert
    )

@router.post("/jobs/analyze-trail-async", response_model=JobSubmissionResponse)
async def analyze_trail_async(request: TrailAnalysisRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    async_jobs[job_id] = {"status": "processing", "result": None}
    background_tasks.add_task(process_long_trail_analysis, job_id, request)
    return JobSubmissionResponse(job_id=job_id, status_url=f"/v1/jobs/status/{job_id}")

@router.get("/jobs/status/{job_id}", response_model=JobStatusResponse)
async def get_job_status(job_id: str):
    job = async_jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")
    return JobStatusResponse(job_id=job_id, status=job["status"], result=job.get("result"))
