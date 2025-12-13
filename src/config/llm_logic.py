import os
from langchain_google_genai import ChatGoogleGenerativeAI

class LLMFactory:
    @staticmethod
    def create_llm():
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is missing. Please check your .env file.")
        
        return ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            verbose=True,
            temperature=0.0, 
            google_api_key=api_key
        )