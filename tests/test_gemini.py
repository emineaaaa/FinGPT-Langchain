import pytest # Profesyonel testler için genellikle bu kullanılır

# 1. Aşama: Veritabanı Testi
def test_supabase_connection():
    try:
        client = db.get_client()
        # Sadece bağlantı ve tablo varlığı kontrolü
        response = client.table("Stocks").select("count", count="exact").limit(1).execute()
        print("✅ DB Bağlantısı ve Tablo Erişimi OK.")
        return True
    except Exception as e:
        print(f"❌ DB Hatası: {e}")
        return False

# 2. Aşama: Model Testi
def test_llm_response():
    try:
        model = get_gemini_model() # Parantezlere dikkat!
        res = model.invoke("Selam, nasılsın?")
        print("✅ LLM Cevap Veriyor.")
        return True
    except Exception as e:
        print(f"❌ LLM Hatası: {e}")
        return False

# 3. Aşama: Akış Testi (Senin yazdığın kısım)
def run_full_integration_test():
    if test_supabase_connection() and test_llm_response():
        print("🚀 Tüm sistemler hazır, entegrasyon testi başlıyor...")

def run_full_integration_test():
    print("\n🔗 Entegrasyon Testi Başlatılıyor...")
    
    # 1. Kontrol: Bağlantılar sağlam mı?
    if not (test_supabase_connection() and test_llm_response()):
        print("❌ Ön testler başarısız. Entegrasyon testi iptal edildi.")
        return

    try:
        # --- ADIM 1: Veri Çekme (Data Fetching) ---
        print("📥 Supabase'den güncel veriler alınıyor...")
        client = db.get_client()
        response = client.table("Stocks").select("*").limit(3).execute()
        raw_data = response.data

        if not raw_data:
            print("⚠️ Veri yok! Test sonlandırıldı.")
            return

        # --- ADIM 2: Prompt ve Zincir Yapılandırması ---
        print("🧠 LangChain zinciri kuruluyor...")
        model = get_gemini_model() # Fonksiyonu çağırıp nesneyi alıyoruz
        
        prompt = ChatPromptTemplate.from_template(
            "Sen FinGPT asistanısın. Elindeki veriler: {data}. "
            "Bu verileri kullanarak profesyonel ama esprili bir piyasa özeti yap."
        )
        
        # Zinciri oluştur (Pipe Operatörü)
        chain = prompt | model

        # --- ADIM 3: Çalıştırma ve Sonuç ---
        print("⚡ Analiz gerçekleştiriliyor...")
        result = chain.invoke({"data": str(raw_data)})

        # --- ADIM 4: Çıktı Doğrulama ---
        if result and result.content:
            print("\n" + "⭐" * 40)
            print("📊 FINGPT ENTEGRASYON BAŞARILI!")
            print("Çıktı Özeti:", result.content[:100], "...") # İlk 100 karakter
            print("⭐" * 40)
        else:
            print("⚠️ Modelden boş yanıt döndü!")

    except Exception as e:
        print(f"💥 Entegrasyon sırasında beklenmedik hata: {e}")

# Dosyanın en altında çalıştırma bloğu
if __name__ == "__main__":
    run_full_integration_test()