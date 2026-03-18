from fastapi import FastAPI
from api.routes import analysis

app = FastAPI(title="FinGPT API", version="1.0.0")

# Router'ı dahil ediyoruz (Registering the Controller)
app.include_router(analysis.router)

@app.get("/")
def home():
    return {"message": "FinGPT Santrali Ayakta!"}