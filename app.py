import streamlit as st
import os
import json
from src.crew import ContentGenCrew
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Kasparro Agentic System", layout="wide")

st.title("Kasparro Agentic Content System (CrewAI Edition)")
st.markdown("This system uses **CrewAI** framework to orchestrate agents for content generation.")

# Sidebar
with st.sidebar:
    st.header("Configuration")
    env_key = os.getenv("GEMINI_API_KEY", "")
    api_key = st.text_input("Gemini API Key", type="password", value=env_key)
    if api_key:
        os.environ["GEMINI_API_KEY"] = api_key

# Input
st.subheader("Input Data")
raw_text = st.text_area("Paste Product Data:", height=200)

if st.button("Launch Crew"):
    if not os.environ.get("GEMINI_API_KEY"):
        st.error("API Key missing.")
        st.stop()
        
    if not raw_text:
        st.warning("Please enter product data.")
        st.stop()

    with st.spinner("Initializing CrewAI Agents..."):
        try:
            crew_engine = ContentGenCrew()
            results = crew_engine.run(raw_text)
            
            st.success("Crew execution complete!")
            
            os.makedirs("output", exist_ok=True)
            tab1, tab2, tab3 = st.tabs(["Product Page", "FAQ Page", "Comparison Page"])
            
            # --- ROBUST OUTPUT HANDLER ---
            def handle_output(data, filename, tab):
                json_data = {}
                
                # Case 1: Pydantic Model (Success)
                if hasattr(data, 'model_dump'):
                    json_data = data.model_dump()
                elif hasattr(data, 'dict'):
                    json_data = data.dict()
                
                # Case 2: Dictionary (Partial Success)
                elif isinstance(data, dict):
                    json_data = data
                
                # Case 3: Raw String (Validation Failed, but we have text)
                else:
                    try:
                        # Try to parse the string as JSON
                        clean_str = str(data).replace("```json", "").replace("```", "")
                        json_data = json.loads(clean_str)
                    except:
                        # If all else fails, show raw text
                        json_data = {"raw_content": str(data)}

                # Save & Display
                with open(f"output/{filename}", "w") as f:
                    json.dump(json_data, f, indent=4)
                
                with tab:
                    st.json(json_data)

            handle_output(results["product_page"], "product_page.json", tab1)
            handle_output(results["faq_page"], "faq_page.json", tab2)
            handle_output(results["comparison_page"], "comparison_page.json", tab3)

        except Exception as e:
            st.error(f"Crew Execution Failed: {str(e)}")