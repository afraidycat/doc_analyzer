"""Configuration settings for the fee simulator."""
import os
from dotenv import load_dotenv
from pathlib import Path
import logging

# Load environment variables
load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Model settings
OPENAI_MODEL = "gpt-4o"
ANTHROPIC_MODEL = "claude-3-haiku-20240307"

def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

# Initialize settings
settings = {
    "OPENAI_API_KEY": OPENAI_API_KEY,
    "ANTHROPIC_API_KEY": ANTHROPIC_API_KEY,
    "OPENAI_MODEL": OPENAI_MODEL,
    "ANTHROPIC_MODEL": ANTHROPIC_MODEL
} 