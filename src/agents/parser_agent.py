import json
from src.agents.base_agent import BaseAgent
from src.models.product_model import ProductData
from src.blocks.extraction_rules import extract_json_from_text

class ParserAgent(BaseAgent):
    def execute(self, raw_text: str) -> ProductData:
        self.log(f"Analyzing text: {raw_text[:30]}...")
        
        # 1. Construct the Prompt with EXPLICIT Formatting Rules
        prompt = f"""
        You are an API that converts product text into structured JSON.
        
        Input Text:
        "{raw_text}"
        
        Rules:
        1. "skin_type", "key_ingredients", and "benefits" MUST be arrays of strings (e.g., ["Oily", "Dry"]).
        2. "concentration" and "side_effects" should be null if not mentioned.
        3. Do not add any markdown formatting (like ```json). Just return the raw JSON object.
        
        Required JSON Schema:
        {{
            "name": "string",
            "concentration": "string or null",
            "skin_type": ["string", "string"],
            "key_ingredients": ["string", "string"],
            "benefits": ["string", "string"],
            "how_to_use": "string",
            "side_effects": "string or null",
            "price": "string"
        }}
        """
        
        # 2. Call Gemini
        response_text = self.call_llm(prompt)
        
        # 3. Clean & Parse JSON
        data = extract_json_from_text(response_text)
        
        if not data:
             # Debugging: Show what failed
            self.log(f"CRITICAL: Failed to extract JSON. LLM Response: {response_text}")
            raise ValueError("LLM returned invalid JSON. Check logs for details.")

        # 4. Validate with Pydantic
        try:
            return ProductData(**data)
        except Exception as e:
            self.log(f"Validation Error: {e}")
            self.log(f"Data received: {data}")
            raise ValueError(f"Pydantic Validation failed: {e}")