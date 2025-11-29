from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class CorrelationsRequest(BaseModel):
    data: List[List[float]]
    columns: Optional[List[str]] = None

class CorrelationsResponse(BaseModel):
    method: str
    columns: List[str]
    matrix: List[List[float]]

class TrendsRequest(BaseModel):
    dates: List[str]
    values: List[float]
    window: int = 7

class TrendsResponse(BaseModel):
    dates: List[str]
    values: List[float]
    moving_avg: List[float]

class InsightsResponse(BaseModel):
    top_factor: str
    insights: List[str]
    stats: Dict[str, Any]
