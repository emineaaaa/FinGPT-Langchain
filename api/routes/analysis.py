from fastapi import APIRouter, HTTPException
from agents.financial_agent import get_pro_analysis
from api.schemas.analysis_schema import AnalysisResponse

router = APIRouter(prefix="/analyze", tags=["Analysis"])

@router.get("/{symbol}", response_model=AnalysisResponse)           #Ben bu fonksiyonun sonunda ne dönersem döneyim, sen onu AnalysisResponse kalıbına sok.

async def analyze_stock(symbol: str):                   #Gemini'ye gideceğiz, DB'ye bakacağız iş biraz uzun sürebilir o yüzden async fonksiyon koyduk bu işlem sırasında başka işlere bakabilirsin ben bitince haber edeceğim sana dedik
    try:
        result = get_pro_analysis(symbol)
        if not result:
            return AnalysisResponse(status="error", symbol=symbol, message="Analiz bulunamadı.")
            
        return AnalysisResponse(status="success", symbol=symbol, data=result) #biz burda aslında Dictionary veriyoz ve en başta response_model belirtmiştik o şekilde döndürecek o yüzden
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))