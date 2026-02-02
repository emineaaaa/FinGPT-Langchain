import os
from supabase import create_client, Client
from core.config import settings
from datetime import datetime


class SupabaseManager:
    def __init__(self):     #magic method
        self.url = settings.SUPABASE_URL
        self.key = settings.SUPABASE_KEY
        self.servicekey = settings.SUPABASE_SERVICE_ROLE_KEY

        if not self.url or not self.servicekey:
            raise ValueError("HATA: SUPABASE_URL veya SUPABASE_SERVICE_ROLE_KEY .env'de tanımlanmamış!")
            
        
        #elindeki URL ve Şifreyi paket yapar ve internet üzerinden Supabase sunucularına gönderir. supabase girişi onaylanırsa bağlantı nesnesi verir sana bir
        self.client: Client = create_client(self.url, self.servicekey)

    def get_client(self) -> Client:
        return self.client
    

    def insert_insight(self, asset_id, symbol, summary, technical_view):
        """AI analizlerini ai_insights tablosuna kaydeder."""
        try:
            data = {
                "asset_id": asset_id,
                "stock_symbol": symbol,
                "summary": summary,
                "technical_view": technical_view,
                "created_at": datetime.now().isoformat()
            }
            return self.client.table("ai_insights").insert(data).execute()
        except Exception as e:
            print(f"Veritabanı kayıt hatası: {e}")
            return None

# projenin her yerinden 'db' diyerek çağırabileceğimiz bir canlı bağlantı nesnesi gibi düşünebiliriz
db = SupabaseManager()

