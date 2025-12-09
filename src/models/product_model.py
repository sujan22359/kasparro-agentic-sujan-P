from pydantic import BaseModel, Field
from typing import List, Optional

class ProductData(BaseModel):
    """The clean internal model for the product."""
    name: str
    price: str
    concentration: Optional[str] = None
    skin_type: List[str] = []
    key_ingredients: List[str] = []
    benefits: List[str] = []
    how_to_use: str
    side_effects: Optional[str] = None

class FAQItem(BaseModel):
    question: str
    answer: str
    category: str

class ComparisonPoint(BaseModel):
    feature: str
    product_a_value: str
    product_b_value: str

class ContentPage(BaseModel):
    """Generic container for final JSON page output."""
    page_type: str
    content: dict