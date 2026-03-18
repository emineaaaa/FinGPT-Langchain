import os
import sys
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.database import db
from core.llm import get_gemini_model 
from langchain_core.messages import SystemMessage, HumanMessage 
from core.indicators import calculate_indicators
from datetime import datetime, timedelta

def analyze_stock_performance(symbol):    

    llm = get_gemini_model(temperature=0.2) 

    #veritabanından son 5 fiyat geçmişi
    response = db.get_client().table("price_history")\
        .select("*")\
        .eq("stock_symbol", symbol)\
        .order("timestamp", desc=True)\
        .limit(30)\
        .execute()
    
    prices = response.data#dict listesi haline getirdik cevapları

    if not prices or len(prices) < 20:
        return None, {"error": f"{symbol} için yeterli teknik veri (min 20) bulunamadı."}
    
    asset_id = prices[0]['asset_id']

    #saf Pandas motorumuzu çalıştırıyoruz
    tech_data = calculate_indicators(prices)

    system_prompt = """
    Sen profesyonel bir finansal analiz robotusun. Sana verilen teknik göstergeleri yorumla.
    Yanıtın SADECE JSON formatında olmalı:
    - "summary": Kısa özet (Örn: RSI aşırı satımda, tepki gelebilir).
    - "technical_view": RSI, SMA ve fiyat trendine dayalı detaylı yorum.
    - "signal": "BUY", "SELL" veya "HOLD" değerlerinden biri.
    - "risk_score": 1 ile 5 arasında bir tam sayı.
    """

    user_content = f"""
    Hisse: {symbol}
    Güncel Fiyat: {tech_data['current_price']}
    RSI (14): {tech_data['rsi']}
    SMA (20): {tech_data['sma_20']}
    Genel Trend: {tech_data['trend']}
    Son Fiyat Geçmişi (Referans): {prices[:5]}
    """

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_content)
    ]

    print(f"Gemini {symbol} için analiz raporu hazırlıyor...")
    

    ai_response = llm.invoke(messages)      #gemşnşye verdim cevap oluşturtmak için
    try:
        #  ```json ... ``` blokları içine koyabilir onları temizliyoruz
        raw_content = ai_response.content.replace("```json", "").replace("```", "").strip()
        analysis_data = json.loads(raw_content)
        
        return asset_id, analysis_data
    except Exception as e:
        print(f"JSON Parse Hatası: {e}")
        return asset_id, None
    
def get_pro_analysis(symbol):
    
    # vt'de son 1 saat içinde yapılmış bir analiz var mı?
    hour_ago = (datetime.now() - timedelta(minutes=15)).isoformat()
    
    existing_insight = db.get_client().table("ai_insights")\
        .select("*")\
        .eq("stock_symbol", symbol)\
        .gte("created_at", hour_ago)\
        .order("created_at", desc=True)\
        .limit(1)\
        .execute()
    
    if existing_insight.data:
        print(f" {symbol} için hazır analiz bulundu, veritabanından getiriliyor...")
        return existing_insight.data[0] # vt'daki satırı dön

    # yoksa gemini analizini yapıyor
    asset_id, data = analyze_stock_performance(symbol)
    
    if asset_id and data:
        # yeni analiz kaydedilir
        db.insert_insight(
            asset_id=asset_id,
            symbol=symbol,
            summary=data['summary'],
            technical_view=data['technical_view']
        )
        print(f"{symbol} analizi kaydedildi.")
        return data
    
    return None


if __name__ == "__main__":
    # test
    hisse = "ARCLK.IS"
    sonuc = get_pro_analysis(hisse)   
    
    if sonuc:
        print(f"\n SONUÇ ({hisse}):")
        print(f"Özet: {sonuc.get('summary')}")
        print(f"Sinyal: {sonuc.get('signal', 'N/A')}") # Sinyal DB sütununda yoksa N/A yazar