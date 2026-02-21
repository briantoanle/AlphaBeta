from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class HoldingBase(BaseModel):
    symbol: str
    weight: float = Field(..., ge=0.0, le=1.0, allow_inf_nan=False)

class PortfolioBase(BaseModel):
    name: str
    holdings: List[HoldingBase] = Field(default_factory=list)
    riskTolerance: float = Field(default=5.0, ge=0.0, allow_inf_nan=False)
    horizon: int = Field(default=10, ge=1)

class MacroScoreResponse(BaseModel):
    score: float
    regime: str
    drivers: List[Dict]
    timestamp: str

class RecommendationResponse(BaseModel):
    recommendations: List[Dict]
