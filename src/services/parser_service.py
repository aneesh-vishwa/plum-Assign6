# src/services/parser_service.py

import re
from typing import Dict, Any

# Define the fields we expect to find in the survey
REQUIRED_FIELDS = ["age", "smoker", "exercise", "diet"]

class IncompleteProfileError(Exception):
    """Custom exception for the >50% missing fields guardrail."""
    pass

def _normalize_value(value: str) -> Any:
    """Converts a string value to its appropriate type (int, bool, or str)."""
    value = value.strip().lower()
    # Convert to boolean
    if value in ["true", "yes", "y"]:
        return True
    if value in ["false", "no", "n"]:
        return False
    # Convert to integer
    if value.isdigit():
        return int(value)
    # Return as a cleaned-up string
    return value

def parse_survey_text(text: str) -> Dict[str, Any]:
    """
    Parses key-value pairs from raw survey text and validates for completeness.
    """
    answers = {}
    # ADD THIS LINE: This will handle newlines typed as "\n" in a single string
    processed_text = text.replace('\\n', '\n')
    
    lines = processed_text.strip().split('\n') # Use the new processed_text variable
    
    # Regex to find key-value pairs, allowing for flexible spacing
    # It looks for a word, followed by a colon, followed by the rest of the line.
    pattern = re.compile(r"^\s*([a-zA-Z]+)\s*:\s*(.+)$")
    
    for line in lines:
        match = pattern.match(line)
        if match:
            key = match.group(1).strip().lower()
            value = match.group(2).strip()
            if key in REQUIRED_FIELDS:
                answers[key] = _normalize_value(value)
    
    # --- GUARDRAIL IMPLEMENTATION ---
    missing_fields_count = 0
    for field in REQUIRED_FIELDS:
        if field not in answers:
            missing_fields_count += 1
            
    if missing_fields_count / len(REQUIRED_FIELDS) > 0.5:
        raise IncompleteProfileError(">50% fields missing")
        
    return answers