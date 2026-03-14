from fastapi import FastAPI, HTTPException
from agents.financial_agent import get_pro_analysis

app = FastAPI(
    title="FinGPT API",
    description="Yapay Zeka Destekli Finansal Analiz Platformu",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "FinGPT API Çalışıyor! Analiz için /analyze/{symbol} adresini kullanın."}

@app.get("/analyze/{symbol}")
async def analyze_stock(symbol: str):
    print(f"📡 API İsteği Geldi: {symbol}")
    try:
        # Senin fonksiyonunu çağırıyoruz
        result = get_pro_analysis(symbol)
        
        # Eğer fonksiyon None döndüyse veya bir sorun oluştuysa
        if result is None:
            raise HTTPException(status_code=404, detail=f"{symbol} için analiz oluşturulamadı.")

        # Senin fonksiyonun her iki durumda da (DB veya AI) 
        # artık bir sözlük (dict) döndüğü için doğrudan paketleyebiliriz
        return {
            "status": "success",
            "symbol": symbol,
            "analysis": result
        }

    except Exception as e:
        # Hata mesajını yakalayıp kullanıcıya gösterelim (Örn: Quota hatası)
        print(f"💥 Hata oluştu: {str(e)}")
        return {
            "status": "error",
            "message": f"Analiz sırasında bir sorun oluştu: {str(e)}"
        }