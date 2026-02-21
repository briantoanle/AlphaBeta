from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class HoldingBase(BaseModel):
    symbol: str
    weight: float = Field(..., ge=0.0, le=1.0, allow_inf_nan=False)

class PortfolioBase(BaseModel):
    name: str
    holdings: List[HoldingBase]
    riskTolerance: float = Field(5.0, ge=0.0, le=10.0)
    horizon: int = Field(10, ge=1, le=100)

class MacroScoreResponse(BaseModel):
    score: float
    regime: str
    drivers: List[Dict]
    timestamp: str

class RecommendationResponse(BaseModel):
    recommendations: List[Dict]
