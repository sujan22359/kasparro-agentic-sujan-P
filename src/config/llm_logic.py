import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

class LLMFactory:
    @staticmethod
    def create_llm():
        api_key = os.getenv("GEMINI_API_KEY")
        model_name = os.getenv("MODEL_NAME", "gemini-2.5-flash")
        
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")

        # CrewAI works best with LangChain's Chat interface
        return ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=api_key,
            temperature=0.1, # Low temp for factual extraction
            convert_system_message_to_human=True
        )