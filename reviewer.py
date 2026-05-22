from groq import Groq
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def review_code(code_snippet):

    prompt = f"""
You are an AI code reviewer.

Analyze this code and return ONLY valid JSON:

{{
    "issue": "",
    "severity": "",
    "confidence": 0,
    "suggestion": ""
}}

Code:
{code_snippet}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except:
        return {
            "issue": "Parsing error",
            "severity": "Low",
            "confidence": 20,
            "suggestion": "Verify manually"
        }
