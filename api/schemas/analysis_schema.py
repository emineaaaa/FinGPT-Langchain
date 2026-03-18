from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


# geminiden gelen inner dto
class AnalysisResult(BaseModel):                      #.NET'teki temel sınıfın gibi düşün. Tüm DTO'lar bundan türemeli.
    summary: str = Field(...)                     #... ile required yapıp description ekleyebilirsin virgül koyarak sona
    technical_view: str
    signal: str
    risk_score: int= Field(..., ge=1, le=5)             #1le 5 arası range verdik (Greater or Equal ve  Less or Equal)


#response dto
class AnalysisResponse(BaseModel):
    status: str
    symbol: str
    data: Optional[Dict[str, Any]] = None            # Gemini'den gelen ham JSON veya bizim modelimiz
    message: Optional[str] = None                       #Optional diyerek nullable yaptık ve eğer veri gelmezse null yap dedik