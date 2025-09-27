import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file or environment variables")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro-vision')  # For multimodal (image+text)
