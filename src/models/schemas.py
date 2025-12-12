from pydantic import BaseModel, Field
from typing import List, Optional

# --- 1. Product Page Model ---
class ProductPage(BaseModel):
    page_type: str = Field(default="product_page")
    name: str
    price: str
    description: str = Field(..., description="A compelling, SEO-friendly marketing description (approx 100 words).")
    key_ingredients: List[str]
    benefits: List[str]
    specs: dict = Field(..., description="Technical specifications like Concentration, Skin Type, etc.")

# --- 2. FAQ Page Model ---
class FAQItem(BaseModel):
    question: str
    answer: str
    category: str

class FAQPage(BaseModel):
    page_type: str = Field(default="faq_page")
    title: str
    q_and_a: List[FAQItem] = Field(..., description="List of at least 15 FAQ items.")

# --- 3. Comparison Page Model ---
class ComparisonRow(BaseModel):
    feature: str
    us: str
    them: str

class ComparisonPage(BaseModel):
    page_type: str = Field(default="comparison_page")
    title: str
    competitor_name: str
    comparison_table: List[ComparisonRow]