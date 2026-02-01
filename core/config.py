import os
from dotenv import load_dotenv          #pythonda .env dosyanın içindeki bilgileri okumasını sağlayar

load_dotenv()           #.env dosysını açar ve içindeki şifreleri hafızaya alır

class Settings:
    PROJECT_NAME: str = "FinGPT-Backend"
    
    SUPABASE_URL: str = os.getenv("SUPABASE_URL")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY")
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")
    SUPABASE_SERVICE_ROLE_KEY: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# Tek bir ayar nesnesi oluşturuyoruz her seferinde her kod pageinden .env çağırıp okumak yerine burda yapıp settings içine attık kullanacağımızda settings ile erişiyoruz.
settings = Settings()