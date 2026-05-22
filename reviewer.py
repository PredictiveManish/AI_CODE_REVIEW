# reviewer.py

from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create Groq client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def review_code(code):

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """
You are a senior software engineer and expert code reviewer.

Review the given code carefully and provide:

1. Bugs or issues
2. Performance improvements
3. Readability improvements
4. Security concerns
5. Best practices
6. Final improved summary
"""
            },
            {
                "role": "user",
                "content": code
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content