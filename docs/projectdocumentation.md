# Kasparro Agentic Content System

A robust, modular AI agent system built with **CrewAI** and **Google Gemini 2.5 Flash**. This application orchestrates a team of autonomous agents to analyze product data, generate strategic FAQs, and create data-driven competitor comparisons.

## Key Features (Engineering Improvements)

* **Modular Architecture:** Agents are defined as dedicated Python classes in `src/agents/`, not monolithic scripts.
* **Deterministic Tools:** Implements `CompetitorLookupTool` to inject consistent market data, preventing hallucination.
* **Strict Output Contracts:** Enforces Pydantic schemas (`ProductPage`, `FAQPage`, `ComparisonPage`) for 100% valid JSON output.
* **Robust Error Handling:** `app.py` includes a smart validation layer that handles schema drifts without crashing the UI.
* **End-to-End Testing:** Includes a full `pytest` suite for schema validation and integration testing.

---

## System Architecture

The project follows a production-grade folder structure:

```text
E:\Kasparro\kasparro-ai-agentic-content-generation-system\
├── src/
│   ├── agents/             # Modular Agent Definitions
│   │   ├── parser_agent.py   (Senior Data Analyst)
│   │   ├── strategy_agent.py (Content Strategist)
│   │   └── writer_agent.py   (Senior Copywriter)
│   ├── tools/              # Custom Tools
│   │   └── search_tools.py   (Competitor Lookup Logic)
│   ├── config/             # Configuration & Factories
│   │   └── llm_logic.py      (Gemini 1.5 Flash Setup)
│   ├── models/             # Pydantic Schemas
│   │   └── schemas.py        (Strict JSON definitions)
│   └── crew.py             # Orchestration Logic
├── tests/                  # CI/CD Testing Suite
│   ├── test_pipeline.py    (End-to-End Integration)
│   └── test_schemas.py     (Unit Tests)
├── app.py                  # Streamlit UI (Robust Rendering)
└── requirements.txt        # Pinned Dependencies
```

## Agents & Roles
### Senior Data Analyst (ParserAgent)

**Goal:**  
Extract factual attributes (Price, Ingredients) with zero hallucination.

**Logic:**  
Enforces strict Pydantic models to ensure data integrity.

---

### Content Strategist (StrategyAgent)

**Goal:**  
Generate high-value FAQ content based on user intent.

**Constraint:**  
Strictly enforces the generation of 20+ questions.

---

### Senior Copywriter (WriterAgent)

**Goal:**  
Create objective comparison tables.

**Tools:**  
Uses `CompetitorLookupTool` to fetch deterministic competitor data instead of guessing.

## Installation & Setup

### 1. Clone the Repository

```bash
    git clone <your-repo-url>
    cd kasparro-ai-agentic-content-generation-system
```
### 2. Install Dependencies
```bash
   pip install -r requirements.txt
```
### 3.Environment Setup Create a `.env` file in the root directory:
```bash
GEMINI_API_KEY=your_google_api_key_here
```
## ▶️ Usage

### Run the Web Application:
``` bash
streamlit run app.py
```
The UI will launch at:  
`http://localhost:8501`

**Steps:**
1. Paste raw product text into the input box.
2. Click **"Launch Crew"**.
3. View results in the **Product**, **FAQ**, and **Comparison** tabs.

## Testing
### This project includes a comprehensive test suite using `pytest`.

**Run All Tests:**
```bash
python -m pytest
```
### Test Coverage:
  - **test_schemas.py**  
  Validates that Pydantic models correctly reject invalid data types.

  - **test_pipeline.py**  
  Runs a live simulation of the CrewAI pipeline to ensure all agents communicate and return files.

---

### Note on Rate Limits

The integration test runs multiple agents rapidly. On the **Google Gemini Free Tier**, you may occasionally encounter a `429 ResourceExhausted` error. This is an API limitation, not a code failure. Retrying after **60 seconds** typically resolves the issue.




