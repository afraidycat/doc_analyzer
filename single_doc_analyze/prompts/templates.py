from single_doc_analyze.models.schemas import DocumentAnalysis

def build_prompt(doc_text: str) -> str:
    return f"""
You are a document analysis expert.

Your task is to:
1. Summarize the document in 3-4 sentences.
2. Identify key topics or themes.
3. Highlight risks, unclear language, or potential issues.
4. Recommend next actions for the user.

Return your response in this exact JSON format:
{{
  "summary": "...",
  "key_topics": ["..."],
  "risks_or_issues": ["..."],
  "recommended_actions": ["..."]
}}

Document text:
---
{doc_text}
---
"""

def build_evaluation_prompt(result: DocumentAnalysis) -> str:
    return f"""
You are a document analysis evaluator. You will be given a structured output and must check if it meets the requirements.

Here is the model's structured output:
---
Summary:
{result.summary}

Key Topics:
{", ".join(result.key_topics)}

Risks or Issues:
{", ".join(result.risks_or_issues)}

Recommended Actions:
{", ".join(result.recommended_actions)}
---

Evaluate if the above response:
1. Includes all 4 required sections
2. Provides specific, useful risks and actions
3. Uses clear, professional language

Return your judgment as JSON:
{{
  "is_acceptable": true or false,
  "feedback": "Short explanation of what is missing or how to improve"
}}
""" 