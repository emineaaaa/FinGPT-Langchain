import pandas as pd
import numpy as np

def calculate_rsi(series, period=14):
    """Kütüphane kullanmadan matematiksel RSI hesaplama"""
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    
    # Sıfıra bölünme hatasını engellemek için küçük bir sabit ekleyelim
    rs = gain / (loss + 1e-9)
    return 100 - (100 / (1 + rs))

def calculate_indicators(price_history):
    """
    Pandas-ta gerektirmeden RSI ve SMA hesaplayan fonksiyon.
    """
    if not price_history or len(price_history) < 20:
        return None

    # 1. Veriyi Pandas DataFrame'e çevir
    df = pd.DataFrame(price_history)
    
    # 2. Tipleri düzenle
    df['price'] = pd.to_numeric(df['price'])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')

    # 3. RSI Hesapla (Kendi yazdığımız fonksiyonla)
    df['rsi'] = calculate_rsi(df['price'], period=14)
    
    # 4. SMA Hesapla (Pandas'ın kendi rolling fonksiyonuyla)
    df['sma_20'] = df['price'].rolling(window=20).mean()

    # Son satırı al
    last_row = df.iloc[-1]
    
    # NaN kontrolü yaparak temiz veri dön
    rsi_val = last_row['rsi']
    sma_val = last_row['sma_20']
    
    return {
        "current_price": float(last_row['price']),
        "rsi": round(float(rsi_val), 2) if pd.notna(rsi_val) else None,
        "sma_20": round(float(sma_val), 2) if pd.notna(sma_val) else None,
        "trend": "BULLISH" if last_row['price'] > sma_val else "BEARISH"
    }