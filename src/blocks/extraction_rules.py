import re
import json

def extract_json_from_text(llm_response: str) -> any:
    """
    Robustly extracts JSON (Object or List) from an LLM response.
    """
    try:
        # 1. Remove Markdown code blocks first
        clean_text = re.sub(r"```json\s*", "", llm_response, flags=re.IGNORECASE)
        clean_text = re.sub(r"```", "", clean_text)
        clean_text = clean_text.strip()

        # 2. Try to find the outermost brackets
        # We look for either [...] for lists or {...} for objects
        match = re.search(r"(\[.*\]|\{.*\})", clean_text, re.DOTALL)
        
        if match:
            potential_json = match.group(1)
            return json.loads(potential_json)
        
        # 3. Fallback: Try parsing the raw text if regex failed
        return json.loads(clean_text)

    except json.JSONDecodeError as e:
        print(f"[Block Error] JSON Decode Error: {e}")
        # Return empty structure to prevent crashes
        return [] if "[" in llm_response else {}
    except Exception as e:
        print(f"[Block Error] Extraction Error: {e}")
        return {}