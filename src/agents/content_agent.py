from src.agents.base_agent import BaseAgent
from src.models.product_model import ProductData, ContentPage

class ContentAgent(BaseAgent):
    def execute(self, product_data: ProductData, strategy_data: dict, page_type: str) -> ContentPage:
        self.log(f"Drafting content for page: {page_type}")

        if page_type == "product_page":
            content = {
                "title": product_data.name,
                "description": f"Experience the power of {product_data.concentration}. {product_data.benefits[0]}.",
                "specs": product_data.dict()
            }
            
        elif page_type == "faq_page":
            content = {
                "title": f"FAQ - {product_data.name}",
                "q_and_a": strategy_data["faq_data"][:5] # Minimum 5 Q&As [cite: 40]
            }
            
        elif page_type == "comparison_page":
            comp_data = strategy_data["competitor_data"]
            content = {
                "title": f"{product_data.name} vs {comp_data['name']}",
                "comparison_table": [
                    {"feature": "Price", "us": product_data.price, "them": comp_data['price']},
                    {"feature": "Ingredients", "us": ", ".join(product_data.key_ingredients), "them": ", ".join(comp_data['key_ingredients'])}
                ]
            }
        else:
            raise ValueError("Unknown page type")

        return ContentPage(page_type=page_type, content=content)