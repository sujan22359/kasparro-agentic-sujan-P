from src.agents.base_agent import BaseAgent
from src.models.product_model import ProductData
from src.blocks.extraction_rules import extract_json_from_text

class StrategyAgent(BaseAgent):
    def execute(self, product_data: ProductData) -> dict:
        self.log("Brainstorming content strategy...")

        # --- Step 1: Generate Questions ---
        q_prompt = f"""
        Generate 5 specific FAQ questions and answers for the product "{product_data.name}".
        Focus on categories: Safety, Usage, and Results.
        
        Return a strict JSON list of objects:
        [
            {{ "category": "Safety", "question": "...", "answer": "..." }}
        ]
        """
        q_response = self.call_llm(q_prompt)
        faq_data = extract_json_from_text(q_response)

        # --- Step 2: Create Fictional Competitor ---
        # FIX: Explicitly ask to match the currency of the input product
        c_prompt = f"""
        Create a fictional competitor product to compare against "{product_data.name}".
        
        IMPORTANT: The price must be in the SAME CURRENCY as {product_data.price} (e.g., if input is ₹, output ₹).
        
        Return JSON:
        {{
            "name": "Fictional Name",
            "price": "Similar Price in matching currency",
            "key_ingredients": ["Ingredient A", "Ingredient B"],
            "benefits": ["Benefit A"]
        }}
        """
        c_response = self.call_llm(c_prompt)
        competitor_data = extract_json_from_text(c_response)

        return {
            "faq_data": faq_data if isinstance(faq_data, list) else [],
            "competitor_data": competitor_data
        }