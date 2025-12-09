from pydantic import BaseModel
from typing import List

class PageTemplate(BaseModel):
    """
    Defines the strict structure a page must follow.
    """
    page_type: str
    sections: List[str] # e.g., ["Header", "Specs", "FAQ"]
    required_fields: List[str] # e.g., ["title", "description"]

# Define standard templates
FAQ_TEMPLATE = PageTemplate(
    page_type="faq", 
    sections=["Title", "Q&A List"], 
    required_fields=["q_and_a"]
)

PRODUCT_TEMPLATE = PageTemplate(
    page_type="product", 
    sections=["Hero", "Details", "Buy Section"], 
    required_fields=["title", "description", "specs"]
)