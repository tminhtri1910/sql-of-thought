import openai
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Get API key from environment
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Create a single client instance
client = openai.OpenAI(api_key=api_key)
