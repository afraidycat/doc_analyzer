from typing import Optional
import openai
from ..models.schemas import DocumentAnalysis
from ..utils.json_utils import parse_json_response
from ..prompts.templates import build_prompt
from ..config import settings

class DocumentAnalyzer:
    def __init__(self):
        self.client = openai.OpenAI()
    
    def analyze(self, doc_text: str, feedback: Optional[str] = None) -> DocumentAnalysis:
        """Analyze document text and return structured analysis."""
        prompt = build_prompt(doc_text)
        if feedback:
            prompt += f"\n\n# Feedback from evaluator:\n{feedback}"
            
        response = self.client.chat.completions.create(
            model=settings["MODEL_NAME"],
            messages=[
                {"role": "system", "content": "You are a document analysis expert."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return parse_json_response(
            response.choices[0].message.content,
            DocumentAnalysis
        ) 