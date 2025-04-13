from langchain_groq import ChatGroq
from models.models import GROQ_MODEL
from dotenv import load_dotenv
import os

# Get the absolute path to the .env file
# env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
# print("Loading .env file from:", env_path)

# # Load environment variables from the explicit path
# load_dotenv(env_path)

# # Debug: Print all environment variables (be careful with sensitive data)
# print("Environment variables loaded:", list(os.environ.keys()))

groq_api_key = os.getenv("GROQ_API_KEY")
if groq_api_key is None:
    groq_api_key = "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"


groq_llm = ChatGroq(temperature=0, groq_api_key=groq_api_key, model_name=GROQ_MODEL)

__all__ = ["groq_llm"]
