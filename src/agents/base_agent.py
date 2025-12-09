import os
import google.generativeai as genai
from abc import ABC, abstractmethod
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name
        self.api_key = os.getenv("GEMINI_API_KEY")
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")

        genai.configure(api_key=self.api_key)
        
        # FIX: Changed model to 'gemini-1.5-flash-latest' which is the stable alias
        # If this still fails, try 'gemini-pro'
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def log(self, message: str):
        print(f"[{self.name}] {message}")

    def call_llm(self, prompt: str) -> str:
        """Calls Gemini API with the provided prompt."""
        try:
            self.log("Sending prompt to Gemini...")
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            self.log(f"Error calling Gemini: {e}")
            # Return empty string or handle error gracefully
            return ""

    @abstractmethod
    def execute(self, input_data):
        pass