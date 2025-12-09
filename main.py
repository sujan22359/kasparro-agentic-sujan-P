import streamlit as st
import json
import os
from src.orchestration.graph import ContentAutomationGraph
from dotenv import load_dotenv

# Load environment variables (for API key)
load_dotenv()

# Set page configuration
st.set_page_config(page_title="Kasparro Content Agent", layout="wide")

# --- UI HEADER ---
st.title("Kasparro Multi-Agent Content System")
st.markdown("""
This system uses **AI Agents** to transform raw product data into structured JSON pages.
**Paste any product text below** to generate a Product Page, FAQ, and Comparison.
""")

# --- SIDEBAR: Configuration ---
with st.sidebar:
    st.header("Configuration")
    
    # API Key Handling
    env_api_key = os.getenv("GEMINI_API_KEY")
    api_key_input = st.text_input("Gemini API Key", value=env_api_key if env_api_key else "", type="password")
    
    if api_key_input:
        os.environ["GEMINI_API_KEY"] = api_key_input
    
    if not os.environ.get("GEMINI_API_KEY"):
        st.warning(" API Key missing! Please set it in .env or here.")
    else:
        st.success(" API Key connected")

    st.divider()
    st.info("System outputs are saved to the `/output` folder.")

# --- MAIN INPUT ---
st.subheader("Input Product Data")
# No default value - purely user input
raw_text = st.text_area(
    "Paste product details here:", 
    height=250,
    placeholder="Example:\nProduct Name: SuperWidget\nPrice: $20\nFeatures: Fast, Durable..."
)

# --- EXECUTION BUTTON ---
if st.button(" Run Agent Pipeline", type="primary"):
    # Input Validation
    if not raw_text.strip():
        st.warning(" Please enter some product text first!")
        st.stop()

    if not os.environ.get("GEMINI_API_KEY"):
        st.error(" Please provide a Gemini API Key to proceed.")
    else:
        # Create a progress container
        status_container = st.container()
        
        with status_container:
            with st.status("Agents are working...", expanded=True) as status:
                try:
                    # 1. Initialize Graph
                    st.write(" Initializing Agents (Parser, Strategy, Content)...")
                    graph = ContentAutomationGraph()
                    
                    # 2. Run Graph (This executes the full pipeline)
                    st.write(" Parsing raw text & developing strategy...")
                    graph.run(raw_text, output_dir="output")
                    
                    status.update(label=" Pipeline Completed Successfully!", state="complete", expanded=False)
                    
                    
                except Exception as e:
                    status.update(label=" Pipeline Failed", state="error")
                    st.error(f"Error details: {e}")
                    st.stop()

        # --- DISPLAY RESULTS (Output Viewer) ---
        st.divider()
        st.header(" Generated Output")
        
        tab1, tab2, tab3 = st.tabs(["Product Page", " FAQ Page", " Comparison Page"])
    
        # Helper to read JSON
        def load_json(filename):
            path = os.path.join("output", filename)
            if os.path.exists(path):
                with open(path, "r") as f:
                    return json.load(f)
            return {"error": "File not found. Did the agents run?"}

        with tab1:
            st.caption("output/product_page.json")
            st.json(load_json("product_page.json"))
            
        with tab2:
            st.caption("output/faq_page.json")
            st.json(load_json("faq_page.json"))
            
        with tab3:
            st.caption("output/comparison_page.json")
            st.json(load_json("comparison_page.json"))