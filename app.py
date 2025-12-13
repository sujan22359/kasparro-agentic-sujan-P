import streamlit as st
import os
import json
import sys
import signal
from src.crew import ContentGenCrew
from dotenv import load_dotenv

# Windows signal fix
if sys.platform == "win32":
    unix_signals = ['SIGHUP', 'SIGQUIT', 'SIGTSTP', 'SIGCONT', 'SIGUSR1', 'SIGUSR2']
    for sig in unix_signals:
        if not hasattr(signal, sig):
            setattr(signal, sig, 1)

load_dotenv()

st.set_page_config(page_title="Kasparro Agentic System", layout="wide")
st.title("Kasparro Agentic Content System ")

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
            
            def handle_output(data, filename, tab):
                json_data = {}
                
                # 1. Best Case: Strict Pydantic Model
                if hasattr(data, 'model_dump'):
                    json_data = data.model_dump()
                elif hasattr(data, 'dict'):
                    json_data = data.dict()
                
                # 2. Good Case: Valid JSON Dictionary
                elif isinstance(data, dict):
                    json_data = data
                
                # 3. Handle Raw String (Prevent Crash)
                # If Strict Parsing failed, we manually parse the JSON to ensure it is valid.
                elif isinstance(data, str):
                    try:
                        clean_text = data.replace("```json", "").replace("```", "").strip()
                        json_data = json.loads(clean_text)
                    except:
                        st.error(f"Could not parse JSON for {filename}")
                        with tab:
                            st.text(data) # Show raw text at least
                        return

                # 4. Handle None
                else:
                    st.error(f"No data returned for {filename}")
                    return

                # Save and Display
                with open(f"output/{filename}", "w") as f:
                    json.dump(json_data, f, indent=4)
                
                with tab:
                    st.json(json_data)

            handle_output(results["product_page"], "product_page.json", tab1)
            handle_output(results["faq_page"], "faq_page.json", tab2)
            handle_output(results["comparison_page"], "comparison_page.json", tab3)

        except Exception as e:
            st.error(f"Crew Execution Failed: {str(e)}")