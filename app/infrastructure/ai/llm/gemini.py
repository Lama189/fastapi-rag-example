from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import get_settings


settings = get_settings()


gemini_llm = ChatGoogleGenerativeAI(
    google_api_key=settings.gemini_llm_api_key,
    model="gemini-3.5-flash",  
    temperature=0.3
)