import json
import os
from openai import OpenAI

DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
MODEL = "deepseek-v4-flash"

def extract_violations_from_document(document_text: str, mock: bool = False) -> dict:
    """
    Extract violations and metadata from a health inspection report.

    When mock=True, returns a predefined dataset for testing
    (the mock response is tailored to the text if 'Green Cafe' appears).
    """
    if mock:
        # Hardcoded extraction for demo; dynamic enough for two facilities
        if "Green Cafe" in document_text:
            return {
                "facility_name": "Green Cafe",
                "jurisdiction": "Los Angeles",
                "inspection_date": "2024-03-16",
                "violations": [
                    {"description": "Mold in ice machine", "severity": "critical"},
                    {"description": "Expired food", "severity": "high"},
                    {"description": "Dirty floors", "severity": "medium"}
                ]
            }
        else:
            return {
                "facility_name": "Sunrise Diner",
                "jurisdiction": "New York City",
                "inspection_date": "2024-03-15",
                "violations": [
                    {"description": "Food not stored at proper temperature", "severity": "critical"},
                    {"description": "Improper handwashing", "severity": "high"},
                    {"description": "No paper towels in restroom", "severity": "low"}
                ]
            }

    client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)
    prompt = f"""
You are a health inspection report parser. Extract the following fields into a single JSON object:
- facility_name: The name of the inspected business location (this is the primary entity being tracked).
- jurisdiction: City/county/state where inspection occurred.
- inspection_date: Date string.
- violations: An array of objects, each with "description" and "severity" (one of: low, medium, high, critical).

Return ONLY valid JSON, no other text.
Report text:
{document_text}
"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a JSON data extractor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
    )
    content = response.choices[0].message.content
    try:
        data = json.loads(content)
        return data
    except json.JSONDecodeError:
        return {"facility_name": "", "jurisdiction": "", "inspection_date": "", "violations": []}
