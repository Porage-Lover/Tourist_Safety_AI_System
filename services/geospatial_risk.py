from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any
import random
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class LocationRequest(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

class RiskScoreResponse(BaseModel):
    latitude: float
    longitude: float
    risk_score: float
    confidence: float
    contributing_factors: Dict[str, Any]

class BatchLocationRequest(BaseModel):
    locations: List[LocationRequest]

class BatchRiskScoreResponse(BaseModel):
    scores: List[RiskScoreResponse]

def get_mock_risk_score(lat: float, lon: float) -> RiskScoreResponse:
    risk = (abs(lat - 13.0827) + abs(lon - 80.2707)) * 10
    risk_score = min(10.0, max(0.0, 10 - risk + random.uniform(-1, 1)))
    confidence = random.uniform(0.85, 0.99)
    factors = {
        "crime_density": random.choice(["low", "medium", "high"]),
        "lighting": random.choice(["good", "poor"]),
    }
    return RiskScoreResponse(
        latitude=lat,
        longitude=lon,
        risk_score=round(risk_score, 2),
        confidence=round(confidence, 2),
        contributing_factors=factors
    )

@router.post("/risk-score/location", response_model=RiskScoreResponse)
async def get_risk_for_location(request: LocationRequest):
    logger.info(f"Received risk score request for Lat: {request.latitude}, Lon: {request.longitude}")
    score_data = get_mock_risk_score(request.latitude, request.longitude)
    return score_data

@router.post("/risk-score/batch", response_model=BatchRiskScoreResponse)
async def get_risk_for_batch_locations(request: BatchLocationRequest):
    logger.info(f"Received batch risk score request for {len(request.locations)} locations.")
    results = [get_mock_risk_score(loc.latitude, loc.longitude) for loc in request.locations]
    return BatchRiskScoreResponse(scores=results)
