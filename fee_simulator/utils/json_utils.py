from typing import Any, TypeVar, Type
import json
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

def clean_json_response(content: str) -> str:
    """Clean JSON response from markdown formatting."""
    content = content.strip()
    if content.startswith("```json"):
        content = content[7:]
    if content.startswith("```"):
        content = content[3:]
    if content.endswith("```"):
        content = content[:-3]
    return content.strip()

def parse_json_response(content: str, model_class: Type[T]) -> T:
    """Parse JSON response into a Pydantic model."""
    try:
        cleaned_content = clean_json_response(content)
        parsed = json.loads(cleaned_content)
        return model_class(**parsed)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON response: {e}")
    except Exception as e:
        raise ValueError(f"Failed to create model instance: {e}") 