import logging
from typing import Optional
import openai
import anthropic
from ..models.schemas import FeeScenarioAnalysis
from ..utils.json_utils import parse_json_response
from ..prompts.templates import build_prompt
from ..config import settings

logger = logging.getLogger(__name__)

class FeeAnalyzer:
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=settings["OPENAI_API_KEY"])
        self.anthropic_client = anthropic.Anthropic(api_key=settings["ANTHROPIC_API_KEY"])
    
    def analyze(self, doc_text: str, provider: str = "openai") -> FeeScenarioAnalysis:
        """Analyze document text and return fee scenarios."""
        prompt = build_prompt(doc_text)
        try:
            content = self._run_llm(prompt, provider)
            return parse_json_response(content, FeeScenarioAnalysis)
        except Exception as e:
            if provider == "anthropic":
                logger.warning("Claude failed. Retrying with OpenAI...")
                content = self._run_llm(prompt, "openai")
                return parse_json_response(content, FeeScenarioAnalysis)
            else:
                raise e
    
    def _run_llm(self, prompt: str, provider: str) -> str:
        """Run the LLM with the specified provider."""
        if provider == "openai":
            response = self.openai_client.chat.completions.create(
                model=settings["OPENAI_MODEL"],
                messages=[
                    {"role": "system", "content": "You are a financial fee analyst AI."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content.strip()
        
        elif provider == "anthropic":
            response = self.anthropic_client.messages.create(
                model=settings["ANTHROPIC_MODEL"],
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text.strip()
        
        else:
            raise ValueError(f"Unsupported provider: {provider}") 