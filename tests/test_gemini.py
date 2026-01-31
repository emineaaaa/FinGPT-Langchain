import os
import sys
from dotenv import load_dotenv


# klasörünü göremez. Bu satır Python'a "ana klasöre bakmayı unutma" der.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.database import db
from core.config import settings
from core.llm import get_gemini_model

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate

load_dotenv()

def test_full_flow():
    print("🚀 FinGPT Test Sistemi Başlatılıyor...")
    
    # --- ADIM 1: Gemini'yi Hazırla ---
    # settings nesnesinden API anahtarını otomatik alır.
    
    try:
        llm =get_gemini_model
        print("Gemini bağlantısı hazır.")
    except Exception as e:
        print(f" Gemini başlatılamadı: {e}")
        return

    try:
        print(f" '{settings.PROJECT_NAME}' projesi için veriler çekiliyor...")
        
        # 'Stocks' senin Supabase'deki tablo adın. Değişikse burayı güncelle!
        response = db.get_client().table("Stocks").select("*").limit(3).execute()
        raw_data = response.data
        
        if not raw_data:
            print("⚠️ Uyarı: Supabase bağlandı ama 'Stocks' tablosu boş gözüküyor!")
            return
        
        print(f"✅ Veri çekme başarılı. Gelen kayıt sayısı: {len(raw_data)}")
    except Exception as e:
        print(f"❌ Supabase hatası: {e}")
        return

    # --- ADIM 3: Gemini ve Veriyi Birleştir (LangChain Zinciri) ---
    try:
        print("🧠 Gemini veriyi senin için yorumluyor...")
        
        prompt = ChatPromptTemplate.from_template(
            "Sen FinGPT asistanısın. Şu an elimizde şu veriler var: {data}. "
            "Bu verilere dayanarak, sanki bir borsa kanalında yorum yapıyormuşsun gibi "
            "kısa, esprili ve teknik bir analiz yap."
        )
        
        # Meşhur Zincirleme (Pipe) Operatörü
        chain = prompt | llm
        
        # Çalıştır ve sonucu al
        result = chain.invoke({"data": str(raw_data)})
        
        print("\n" + "="*30)
        print("📊 FINGPT ANALİZ SONUCU:")
        print("="*30)
        print(result.content)
        print("="*30 + "\n")
        
    except Exception as e:
        print(f"❌ Analiz sırasında hata oluştu: {e}")

if __name__ == "__main__":
    test_full_flow()