from pydantic import BaseModel
from typing import List
from pypdf import PdfReader
import openai
import gradio as gr
import json
import os
from dotenv import load_dotenv

load_dotenv()  # Load your OpenAI API key from .env file

# 🧱 Define the structure of the AI output using Pydantic
class DocumentAnalysis(BaseModel):
    summary: str
    key_topics: List[str]
    risks_or_issues: List[str]
    recommended_actions: List[str]

# 🧪 Evaluator Agent Schema
class EvaluationResult(BaseModel):
    is_acceptable: bool
    feedback: str

# 🧠 Prompt for the document analyzer agent
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

# 🧠 Prompt for evaluator agent
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

# 📄 Extract text from PDF
def extract_text_from_pdf(pdf_file) -> str:
    reader = PdfReader(pdf_file)
    full_text = ""
    for page in reader.pages:
        if page.extract_text():
            full_text += page.extract_text() + "\n"
    return full_text.strip()

# 🧠 Run document analyzer agent
def analyze_document(doc_text: str) -> DocumentAnalysis:
    prompt = build_prompt(doc_text)
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a document analysis expert."},
            {"role": "user", "content": prompt}
        ]
    )
    content = response.choices[0].message.content.strip()

    # Remove markdown code block formatting if present
    if content.startswith("```json"):
        content = content[7:]
    if content.startswith("```"):
        content = content[3:]
    if content.endswith("```"):
        content = content[:-3]
    content = content.strip()

    try:
        parsed = json.loads(content)
        return DocumentAnalysis(**parsed)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        print(f"Content that failed to parse: {content}")
        raise Exception("Failed to get valid JSON response from GPT. Please try again.")

# 🧪 Run evaluator agent
def evaluate_output(result: DocumentAnalysis) -> EvaluationResult:
    eval_prompt = build_evaluation_prompt(result)
    eval_response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a quality evaluator for document analysis outputs."},
            {"role": "user", "content": eval_prompt}
        ]
    )
    raw_eval = eval_response.choices[0].message.content.strip()

    if raw_eval.startswith("```json"):
        raw_eval = raw_eval[7:]
    if raw_eval.startswith("```"):
        raw_eval = raw_eval[3:]
    if raw_eval.endswith("```"):
        raw_eval = raw_eval[:-3]
    raw_eval = raw_eval.strip()

    try:
        parsed = json.loads(raw_eval)
        return EvaluationResult(**parsed)
    except Exception as e:
        raise Exception("Evaluation agent failed to parse output. Check prompt formatting.") from e

# 🧠 Agent loop: analyze → evaluate → retry if needed
def process_document(file):
    text = extract_text_from_pdf(file)

    # Step 1: First pass
    result = analyze_document(text)

    # Step 2: Evaluate
    evaluation = evaluate_output(result)

    # Step 3: Retry if unacceptable
    if not evaluation.is_acceptable:
        print("⚠️ Evaluation failed. Retrying with feedback...")

        prompt_with_feedback = build_prompt(text) + f"\n\n# Feedback from evaluator:\n{evaluation.feedback}\n\nPlease revise your output accordingly."

        retry_response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a document analysis expert."},
                {"role": "user", "content": prompt_with_feedback}
            ]
        )
        retry_content = retry_response.choices[0].message.content.strip()

        if retry_content.startswith("```json"):
            retry_content = retry_content[7:]
        if retry_content.startswith("```"):
            retry_content = retry_content[3:]
        if retry_content.endswith("```"):
            retry_content = retry_content[:-3]
        retry_content = retry_content.strip()

        try:
            parsed_retry = json.loads(retry_content)
            result = DocumentAnalysis(**parsed_retry)
        except json.JSONDecodeError as e:
            return f"❌ Retry failed: Could not parse improved output. Feedback was: {evaluation.feedback}"

    # Step 4: Final return
    return f"""
📄 **Summary**
{result.summary}

🔑 **Key Topics**
{', '.join(result.key_topics)}

⚠️ **Risks or Issues**
{', '.join(result.risks_or_issues)}

✅ **Recommended Actions**
{', '.join(result.recommended_actions)}
"""

# 🚀 Launch Gradio UI
if __name__ == "__main__":
    gr.Interface(
        fn=process_document,
        inputs=gr.File(label="Upload PDF"),
        outputs="text",
        title="One-Shot Document Analyzer",
        description="Upload a document and receive a structured summary with risks and action items."
    ).launch()