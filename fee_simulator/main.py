from pydantic import BaseModel
from typing import List
from pypdf import PdfReader
import openai
import gradio as gr
import json
import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env from shared root
load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / ".env")

# 1️⃣ Pydantic schema for fee scenario output
class FeeScenario(BaseModel):
    participant_type: str
    volume_tier: str
    order_type: str
    estimated_fee: str
    rebate: str
    notes: str

class FeeScenarioAnalysis(BaseModel):
    scenarios: List[FeeScenario]

# 2️⃣ Prompt generator for fee scenario logic
def build_prompt(doc_text: str) -> str:
    return f"""
You are a financial pricing analyst AI. Given the exchange fee schedule below:

1. Identify participant types, volume tiers, and order types
2. Generate 3–5 realistic example scenarios showing estimated fees and rebates
3. Provide short notes explaining how each result was derived

Return your response in this JSON format:
{{
  "scenarios": [
    {{
      "participant_type": "...",
      "volume_tier": "...",
      "order_type": "...",
      "estimated_fee": "...",
      "rebate": "...",
      "notes": "..."
    }}
  ]
}}

Document:
---
{doc_text}
---
"""

# 3️⃣ PDF text extractor
def extract_text_from_pdf(pdf_file) -> str:
    reader = PdfReader(pdf_file)
    full_text = ""
    for page in reader.pages:
        if page.extract_text():
            full_text += page.extract_text() + "\n"
    return full_text.strip()

# 4️⃣ LLM call + JSON parsing
def analyze_document(doc_text: str) -> FeeScenarioAnalysis:
    prompt = build_prompt(doc_text)
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a financial fee analyst AI."},
            {"role": "user", "content": prompt}
        ]
    )
    content = response.choices[0].message.content.strip()

    if content.startswith("```json"):
        content = content[7:]
    if content.startswith("```"):
        content = content[3:]
    if content.endswith("```"):
        content = content[:-3]
    content = content.strip()

    parsed = json.loads(content)
    return FeeScenarioAnalysis(**parsed)

# 5️⃣ Gradio app logic
def process_document(file):
    text = extract_text_from_pdf(file)
    result = analyze_document(text)

    output = "📊 **Fee Scenario Variations**\n\n"
    for scenario in result.scenarios:
        output += f"""
🧾 **{scenario.participant_type} - {scenario.order_type}**
- Tier: {scenario.volume_tier}
- Fee: {scenario.estimated_fee}
- Rebate: {scenario.rebate}
- Notes: {scenario.notes}

"""
    return output

# 6️⃣ Launch the app
if __name__ == "__main__":
    gr.Interface(
        fn=process_document,
        inputs=gr.File(label="Upload Exchange Fee Schedule (PDF)"),
        outputs="text",
        title="Fee Simulator Agent",
        description="Upload a document and receive 3–5 estimated fee and rebate scenarios."
    ).launch()