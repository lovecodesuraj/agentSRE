try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    print("Successfully imported ChatGoogleGenerativeAI")
except ImportError as e:
    print(f"Error importing ChatGoogleGenerativeAI: {str(e)}")
    raise

from dotenv import load_dotenv
import os
from models.models import GEMINI_MODEL

print("GEMINI_MODEL:", GEMINI_MODEL)

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if api_key is None:
    api_key = "AIzaSyDCASZ4nMCbPOd_0FMm4ZtZYUzLZbw2JEQ"

print("Using API key:", api_key[:5] + "..." if api_key else "None")

try:
    gemini_llm = ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=api_key,
        # other params...
    )
    print("Successfully created gemini_llm")
except Exception as e:
    print(f"Error creating gemini_llm: {str(e)}")
    raise

__all__ = ["gemini_llm"]
