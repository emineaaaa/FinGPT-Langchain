import yfinance as yf
from core.database import db
from datetime import datetime

def fetch_and_update_assets():
    try:
        print(" Supabase 'assets' tablosu okunuyor...")
        # bize sadece iki id belirtecek column yeterli performans açısından ikisini select ettik
        response = db.get_client().table("assets").select("id, symbol").execute()
        assets = response.data
        #assets Dictionary veri tipinde dönüyor (list of Dictionaries)

        if not assets:
            print("Güncellenecek varlık bulunamadı.")
            return

        for asset in assets:
            symbol = asset['symbol'] 
            asset_id = asset['id']
            
            print(f"🔄 {symbol} için veriler çekiliyor...")
            ticker = yf.Ticker(symbol)
            fast_info = ticker.fast_info
            
            # Yahoo Finance'den temel verileri alıyoruz
            current_price = fast_info['last_price']
            # Değişim oranını hesaplayalım (yfinance üzerinden)
            prev_close = fast_info['previous_close']
            change_24h = ((current_price - prev_close) / prev_close) * 100 if prev_close else 0
            volume = fast_info['last_volume']

            # 1. ADIM: price_history tablosuna detaylı kayıt atıyoruz
            # Senin tablonda 'stock_symbol' ve 'price' sütunları var, onları besliyoruz
            db.get_client().table("price_history").insert({
                "asset_id": asset_id,
                "stock_symbol": symbol,
                "price": current_price,
                "change_24h": change_24h,
                "volume": volume,
                "timestamp": datetime.now().isoformat()
            }).execute()

            print(f"✅ {symbol} geçmiş tablosuna eklendi: {current_price:.2f} TL")

        print("\n Veri çekme ve senkronizasyon işlemi başarıyla tamamlandı!")

    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    fetch_and_update_assets()