
from core.config import settings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

def get_gemini_model(model_name="gemini-1.5-flash", temperature=0.6):
    return ChatGoogleGenerativeAI(
        model=model_name,
        temperature=temperature,
        google_api_key=settings.GOOGLE_API_KEY 

    )

def get_openai_model(model_name, temperature):
    return  ChatOpenAI(
        model=model_name,
        temperature=temperature,
        openai_api_key=settings.OPENAI_API_KEY
    )
