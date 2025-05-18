"""Configuration settings for the document analysis application."""
import os
from dotenv import load_dotenv
import logging
from typing import Optional

# Load environment variables
load_dotenv()

# Application settings
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
MODEL_NAME = os.getenv('MODEL_NAME', 'gpt-4o')
MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))

# Optional API keys
anthropic_api_key: Optional[str] = None
google_api_key: Optional[str] = None
deepseek_api_key: Optional[str] = None
groq_api_key: Optional[str] = None
grok_api_key: Optional[str] = None

def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

# Initialize settings
settings = {
    "OPENAI_API_KEY": OPENAI_API_KEY,
    "MODEL_NAME": MODEL_NAME,
    "MAX_RETRIES": MAX_RETRIES,
    "anthropic_api_key": anthropic_api_key,
    "google_api_key": google_api_key,
    "deepseek_api_key": deepseek_api_key,
    "groq_api_key": groq_api_key,
    "grok_api_key": grok_api_key
} 