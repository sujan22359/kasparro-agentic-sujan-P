import pytest
from src.models.schemas import ProductPage, FAQPage, ComparisonPage

# --- Test 1: Product Page Validation ---
def test_product_page_structure():
    """
    Verifies that the ProductPage model correctly accepts valid data
    and rejects missing required fields.
    """
    valid_data = {
        "page_type": "product_page",
        "name": "Test Serum",
        "price": "$20",
        "description": "A great serum.",
        "key_ingredients": ["Vit C", "Water"],
        "benefits": ["Glow", "Smooth"],
        "specs": {"volume": "30ml"}
    }
    
    # Should pass without error
    model = ProductPage(**valid_data)
    assert model.name == "Test Serum"
    assert len(model.key_ingredients) == 2

    # Should fail if description is missing
    with pytest.raises(ValueError):
        invalid_data = valid_data.copy()
        del invalid_data["description"]
        ProductPage(**invalid_data)

# --- Test 2: FAQ Constraint Validation ---
def test_faq_page_validation():
    """
    Tests that the FAQPage model can handle a list of questions.
    """
    faq_data = {
        "page_type": "faq_page",
        "title": "FAQ Section",
        "q_and_a": [
            {"question": "Q1", "answer": "A1", "category": "Usage"},
            {"question": "Q2", "answer": "A2", "category": "Safety"}
        ]
    }
    
    model = FAQPage(**faq_data)
    assert len(model.q_and_a) == 2
    assert model.q_and_a[0].category == "Usage"

# --- Test 3: Comparison Page Logic ---
def test_comparison_page_structure():
    """
    Ensures the ComparisonPage correctly structures the table data.
    """
    comp_data = {
        "page_type": "comparison_page",
        "title": "Us vs Them",
        "competitor_name": "Brand X",
        "comparison_table": [
            {"feature": "Price", "us": "$10", "them": "$15"},
            {"feature": "Size", "us": "50ml", "them": "30ml"}
        ]
    }
    
    model = ComparisonPage(**comp_data)
    assert model.competitor_name == "Brand X"
    assert model.comparison_table[0].us == "$10"