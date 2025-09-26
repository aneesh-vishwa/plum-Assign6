# src/utils/schemas.py

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class HealthProfileResponse(BaseModel):
    """
    Defines the final JSON output for a successful health profile generation.
    """
    risk_level: str = Field(..., example="high")
    factors: List[str] = Field(..., example=["smoking", "poor diet", "low exercise"])
    recommendations: List[str] = Field(..., example=["Quit smoking", "Reduce sugar", "Walk 30 mins daily"])
    status: str = Field(default="ok")

class ErrorResponse(BaseModel):
    """
    Defines the JSON output for guardrails or errors.
    """
    status: str = Field(..., example="incomplete_profile")
    reason: str = Field(..., example=">50% fields missing")