from pydantic import BaseModel
from typing import List, Dict, Optional

class HoldingBase(BaseModel):
    symbol: str
    weight: float

class PortfolioBase(BaseModel):
    name: str
    holdings: List[HoldingBase]
    riskTolerance: float = 5.0
    horizon: int = 10

class MacroScoreResponse(BaseModel):
    score: float
    regime: str
    drivers: List[Dict]
    timestamp: str

class RecommendationResponse(BaseModel):
    recommendations: List[Dict]
