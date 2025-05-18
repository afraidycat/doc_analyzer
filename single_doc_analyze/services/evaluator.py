from typing import Optional
import openai
from ..models.schemas import DocumentAnalysis, EvaluationResult
from ..utils.json_utils import parse_json_response
from ..prompts.templates import build_evaluation_prompt
from ..config import settings

class DocumentEvaluator:
    def __init__(self):
        self.client = openai.OpenAI()
    
    def evaluate(self, result: DocumentAnalysis) -> EvaluationResult:
        """Evaluate the document analysis output."""
        prompt = build_evaluation_prompt(result)
        
        response = self.client.chat.completions.create(
            model=settings["MODEL_NAME"],
            messages=[
                {"role": "system", "content": "You are a quality evaluator for document analysis outputs."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return parse_json_response(
            response.choices[0].message.content,
            EvaluationResult
        ) 