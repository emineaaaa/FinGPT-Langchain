import os
import sys

# Proje kök dizinini Python yoluna ekle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.database import db
from core.llm import get_gemini_model
from langchain_core.prompts import ChatPromptTemplate

# 1. Aşama: Veritabanı Testi
def test_supabase_connection():
    try:
        client = db.get_client()
        # Tablo adını 'assets' olarak güncelledik
        response = client.table("assets").select("count", count="exact").limit(1).execute()
        print("✅ DB Bağlantısı ve 'assets' Tablosuna Erişim OK.")
        return True
    except Exception as e:
        print(f"❌ DB Hatası: {e}")
        return False

# 2. Aşama: Model Testi
def test_llm_response():
    try:
        model = get_gemini_model()
        res = model.invoke("Selam, nasılsın?")
        print("✅ LLM (Gemini) Cevap Veriyor.")
        return True
    except Exception as e:
        print(f"❌ LLM Hatası: {e}")
        return False

# 3. Aşama: Entegrasyon Akış Testi
def run_full_integration_test():
    print("\n🔗 FINGPT ENTEGRASYON TESTİ BAŞLATILIYOR...")
    print("-" * 40)
    
    # Adım 0: Bağlantı Kontrolleri
    if not (test_supabase_connection() and test_llm_response()):
        print("\n❌ Ön testler başarısız. Entegrasyon testi iptal edildi.")
        return

    try:
        # Adım 1: Veri Çekme
        print("\n📥 Supabase'den güncel veriler alınıyor...")
        client = db.get_client()
        # Tablo adını 'assets' olarak güncelledik
        response = client.table("assets").select("*").limit(3).execute()
        raw_data = response.data

        if not raw_data:
            print("⚠️ 'assets' tablosu boş! Lütfen önce tools/bulk_insert.py çalıştır.")
            return

        # Adım 2: LangChain Zinciri
        print("🧠 LangChain zinciri kuruluyor...")
        model = get_gemini_model()
        
        prompt = ChatPromptTemplate.from_template(
            "Sen FinGPT asistanısın. Elindeki veriler: {data}. "
            "Bu verileri kullanarak profesyonel ama esprili bir piyasa özeti yap."
        )
        
        chain = prompt | model

        # Adım 3: Çalıştırma
        print("⚡ Gemini analizi gerçekleştiriyor...")
        result = chain.invoke({"data": str(raw_data)})

        # Adım 4: Doğrulama
        if result and result.content:
            print("\n" + "⭐" * 45)
            print("🚀 FINGPT SİSTEMİ TAMAMEN ÇALIŞIR DURUMDA!")
            print(f"Modelden Gelen Özet: {result.content[:150]}...")
            print("⭐" * 45)
        else:
            print("⚠️ Modelden boş yanıt döndü!")

    except Exception as e:
        print(f"💥 Test sırasında beklenmedik hata oluştu: {e}")

if __name__ == "__main__":
    run_full_integration_test()