from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel, Field
from typing import List, Tuple
from geojson_pydantic import Feature, FeatureCollection, Polygon
import random
from datetime import datetime

router = APIRouter()

class PredictiveHotspotProperties(BaseModel):
    predicted_risk_level: float
    confidence_interval: Tuple[float, float]
    crime_type: str
    valid_from: datetime
    valid_to: datetime

def generate_mock_hotspots(bbox: Tuple[float, float, float, float], start_time: datetime, end_time: datetime, crime_type: str) -> FeatureCollection:
    features = []
    min_lon, min_lat, max_lon, max_lat = bbox
    for _ in range(random.randint(2, 5)):
        lon_start = random.uniform(min_lon, max_lon - 0.005)
        lat_start = random.uniform(min_lat, max_lat - 0.005)
        poly_coords = [[
            (lon_start, lat_start),
            (lon_start + 0.002, lat_start + 0.001),
            (lon_start + 0.001, lat_start + 0.003),
            (lon_start, lat_start)
        ]]
        risk = random.uniform(5.0, 9.5)
        properties = PredictiveHotspotProperties(
            predicted_risk_level=round(risk, 2),
            confidence_interval=(round(risk - 1.5, 2), round(risk + 1.5, 2)),
            crime_type=crime_type,
            valid_from=start_time,
            valid_to=end_time
        )
        features.append(Feature(geometry=Polygon(coordinates=poly_coords), properties=properties.dict()))
    return FeatureCollection(features=features)

@router.get("/predictive-hotspots", response_model=FeatureCollection)
async def get_predictive_hotspots(
    start_time: datetime,
    end_time: datetime,
    crime_type: str,
    bbox: str = Query(..., regex=r"^-?\d+\.?\d*,-?\d+\.?\d*,-?\d+\.?\d*,-?\d+\.?\d*$", description="min_lon,min_lat,max_lon,max_lat")
):
    try:
        bbox_coords = tuple(map(float, bbox.split(',')))
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid bbox format.")
    hotspots = generate_mock_hotspots(bbox_coords, start_time, end_time, crime_type)
    return hotspots
