import pytest
import os
from dotenv import load_dotenv

# --- THE FIX: Load the API Key before running tests ---
load_dotenv()

from src.crew import ContentGenCrew
from src.models.schemas import ProductPage, FAQPage

@pytest.mark.integration
def test_full_crew_execution():
    """
    Runs the actual CrewAI pipeline with dummy text to verify 
    that agents execute and return non-empty data.
    """
    # Verify key is loaded (Debugging safety)
    if not os.getenv("GEMINI_API_KEY"):
        pytest.fail("GEMINI_API_KEY not found. Make sure .env file exists.")

    # 1. Setup Dummy Data
    raw_text = """
    Product Name: Test Vitamin C
    Price: INR 100
    Ingredients: Water, Vitamin C
    Benefits: Glow
    """

    # 2. Run the Crew
    crew = ContentGenCrew()
    results = crew.run(raw_text)

    # 3. Verify Product Page Output
    # We accept either a Pydantic model OR a valid raw string (the fallback)
    product_out = results['product_page']
    assert product_out is not None
    if hasattr(product_out, 'name'):
        assert "Test" in product_out.name
    else:
        # If it returned raw text/dict, check content exists
        assert "Test" in str(product_out)

    # 4. Verify FAQ Page Output
    faq_out = results['faq_page']
    assert faq_out is not None
    # Check that we got data back
    assert len(str(faq_out)) > 0 

    # 5. Verify Comparison Output (Tool Usage)
    comp_out = results['comparison_page']
    assert comp_out is not None