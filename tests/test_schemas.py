import pytest
from pydantic import ValidationError
from src.models.schemas import ProductPage, FAQPage

# --- Test 1: Product Page Constraints ---
def test_product_page_validation():
    """Ensures ProductPage rejects empty data and accepts valid data."""
    valid_data = {
        "page_type": "product_page",
        "name": "Test Serum",
        "price": "INR 500",
        "description": "A great serum.",
        "key_ingredients": ["Vit C"],
        "benefits": ["Glow"],
        "specs": {"volume": "30ml"}
    }
    model = ProductPage(**valid_data)
    assert model.name == "Test Serum"

    # Fail case: Missing required field 'name'
    with pytest.raises(ValidationError):
        invalid_data = valid_data.copy()
        del invalid_data["name"]
        ProductPage(**invalid_data)

# --- Test 2: FAQ Page Constraints ---
def test_faq_page_structure():
    """Ensures FAQPage correctly structures the Q&A list."""
    data = {
        "page_type": "faq_page",
        "title": "FAQs",
        "q_and_a": [
            {"question": "Q1", "answer": "A1", "category": "Usage"},
            {"question": "Q2", "answer": "A2", "category": "Safety"}
        ]
    }
    model = FAQPage(**data)
    assert len(model.q_and_a) == 2
    assert model.q_and_a[0].category == "Usage"