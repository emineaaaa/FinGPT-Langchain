from fastapi import APIRouter, HTTPException
from agents.financial_agent import get_pro_analysis
from api.schemas.analysis_schema import AnalysisResponse

router = APIRouter(prefix="/analyze", tags=["Analysis"])

@router.get("/{symbol}", response_model=AnalysisResponse)
async def analyze_stock(symbol: str):
    try:
        result = get_pro_analysis(symbol)
        if not result:
            return AnalysisResponse(status="error", symbol=symbol, message="Analiz bulunamadı.")
            
        return AnalysisResponse(status="success", symbol=symbol, data=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))