from pydantic import BaseModel
from typing import Optional, Dict, Any

class AnalysisResult(BaseModel):
    summary: str
    technical_view: str
    signal: str
    risk_score: int

class AnalysisResponse(BaseModel):
    status: str
    symbol: str
    data: Optional[Dict[str, Any]] = None # Gemini'den gelen ham JSON veya bizim modelimiz
    message: Optional[str] = None