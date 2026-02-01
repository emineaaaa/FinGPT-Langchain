import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.database import db


def bulk_insert_assets():
    popular_stocks = [
    # Bankacılık ve Finans
    {"symbol": "AKBNK.IS", "name": "Akbank", "type": "stock"},
    {"symbol": "GARAN.IS", "name": "Garanti BBVA", "type": "stock"},
    {"symbol": "ISCTR.IS", "name": "İş Bankası (C)", "type": "stock"},
    {"symbol": "YKBNK.IS", "name": "Yapı Kredi Bankası", "type": "stock"},
    {"symbol": "HALKB.IS", "name": "Halkbank", "type": "stock"},
    {"symbol": "VAKBN.IS", "name": "Vakıfbank", "type": "stock"},
    
    # Sanayi ve Enerji
    {"symbol": "EREGL.IS", "name": "Erdemir Demir Çelik", "type": "stock"},
    {"symbol": "KRDMD.IS", "name": "Kardemir (D)", "type": "stock"},
    {"symbol": "ASELS.IS", "name": "Aselsan", "type": "stock"},
    {"symbol": "THYAO.IS", "name": "Türk Hava Yolları", "type": "stock"},
    {"symbol": "TUPRS.IS", "name": "Tüpraş", "type": "stock"},
    {"symbol": "PETKM.IS", "name": "Petkim", "type": "stock"},
    {"symbol": "SASA.IS", "name": "Sasa Polyester", "type": "stock"},
    {"symbol": "HEKTS.IS", "name": "Hektaş", "type": "stock"},
    {"symbol": "ASTOR.IS", "name": "Astor Enerji", "type": "stock"},
    {"symbol": "KONTR.IS", "name": "Kontrolmatik", "type": "stock"},
    
    # Holdingler ve Perakende
    {"symbol": "KCHOL.IS", "name": "Koç Holding", "type": "stock"},
    {"symbol": "SAHOL.IS", "name": "Sabancı Holding", "type": "stock"},
    {"symbol": "SISE.IS", "name": "Şişecam", "type": "stock"},
    {"symbol": "BIMAS.IS", "name": "BİM Mağazalar", "type": "stock"},
    {"symbol": "MGROS.IS", "name": "Migros", "type": "stock"},
    {"symbol": "ARCLK.IS", "name": "Arçelik", "type": "stock"},
    {"symbol": "FROTO.IS", "name": "Ford Otosan", "type": "stock"},
    {"symbol": "TOASO.IS", "name": "Tofaş", "type": "stock"},
    
    # Gayrimenkul ve Diğer
    {"symbol": "EKGYO.IS", "name": "Emlak Konut GYO", "type": "stock"},
    {"symbol": "TCELL.IS", "name": "Turkcell", "type": "stock"},
    {"symbol": "TTKOM.IS", "name": "Türk Telekom", "type": "stock"},
    {"symbol": "ENKAI.IS", "name": "Enka İnşaat", "type": "stock"},
    {"symbol": "PNSUT.IS", "name": "Pınar Süt", "type": "stock"},
    {"symbol": "DOAS.IS", "name": "Doğuş Otomotiv", "type": "stock"},
    
    # Kripto 
    {"symbol": "BTC-USD", "name": "Bitcoin", "type": "crypto"},
    {"symbol": "ETH-USD", "name": "Ethereum", "type": "crypto"}
]

    try:
        print(f"Toplam {len(popular_stocks)} varlık tablodan kontrol ediliyor...")
        
        for stock in popular_stocks:
            #sembol zaten var mı diye kontrol 
            check = db.get_client().table("assets").select("id").eq("symbol", stock["symbol"]).execute()
            
            if not check.data:
                db.get_client().table("assets").insert({
                    "symbol": stock["symbol"],
                    "name": stock["name"],
                    "asset_type": stock["type"]
                }).execute()
                print(f"Eklendi: {stock['symbol']}")
            else:
                print(f"Zaten var: {stock['symbol']}")

        print("\n İşlem tamamlandı")

    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    bulk_insert_assets()