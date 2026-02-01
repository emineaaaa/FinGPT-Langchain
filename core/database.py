import os
from supabase import create_client, Client
from core.config import settings


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

# projenin her yerinden 'db' diyerek çağırabileceğimiz bir canlı bağlantı nesnesi gibi düşünebiliriz
db = SupabaseManager()

