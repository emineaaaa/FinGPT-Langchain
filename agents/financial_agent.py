import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.database import db
from core.llm import get_gemini_model 
from langchain_core.messages import SystemMessage, HumanMessage 
def analyze_stock_performance(symbol):    

    llm = get_gemini_model(temperature=0.3) 

    #veritabanından son 5 fiyat geçmişi
    response = db.get_client().table("price_history")\
        .select("*")\
        .eq("stock_symbol", symbol)\
        .order("timestamp", desc=True)\
        .limit(5)\
        .execute()
    
    prices = response.data#dict listesi haline getirdik cevapları

    if not prices:
        return f"{symbol} için analiz edilecek veri bulunamadı."
    
    asset_id = prices[0]['asset_id']

    messages = [
        SystemMessage(content="""
            Sen FinGPT'nin kıdemli borsa analistisin. 
            Verileri teknik analiz yöntemleriyle yorumlar, kısa ve öz bilgi verirsin.
            Asla yatırım tavsiyesi vermez, teknik görünümü raporlarsın.
        """),           #bu kısım bir ön koşullandırma kısmıydı aslında
        HumanMessage(content=f"{symbol} hissesinin son 5 verisi: {prices}. Bu verileri analiz et.")     #kullanıcı tarafı, soru ve veri
    ]

    print(f"Gemini {symbol} için analiz raporu hazırlıyor...")
    

    ai_response = llm.invoke(messages)      #gemşnşye verdim cevap oluşturtmak için
    return asset_id, ai_response.content     #uzun cevabın analiz metninin alıyoruz



if __name__ == "__main__":
    # test
    hisse="THYAO.IS"
    asset_id, rapor = analyze_stock_performance(hisse)

    
    print(f"GEMINI'NIN CEVABI ({hisse}):")
    print(rapor)

    db.insert_insight(
            asset_id=asset_id,
            symbol=hisse,
            summary=rapor[:200], #ilk 200 karakter 
            technical_view=rapor
        )
    
