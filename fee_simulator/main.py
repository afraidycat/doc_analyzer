from pydantic import BaseModel
from typing import List
from pypdf import PdfReader
import json
import os
from dotenv import load_dotenv
from pathlib import Path
import gradio as gr

# Load environment variables
load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / ".env")

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# 1️⃣ Output Schema
class FeeScenario(BaseModel):
    participant_type: str
    volume_tier: str
    order_type: str
    estimated_fee: str
    rebate: str
    notes: str

class FeeScenarioAnalysis(BaseModel):
    scenarios: List[FeeScenario]

# 2️⃣ Prompt Builder
def build_prompt(doc_text: str) -> str:
    return f"""
You are a financial pricing analyst AI. Given the exchange fee schedule below:

1. Identify participant types, volume tiers, and order types
2. Generate 3–5 realistic example scenarios showing estimated fees and rebates
3. Provide short notes explaining how each result was derived

Return ONLY your response in this exact JSON format (no explanation, no Markdown):
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

# 3️⃣ PDF Reader
def extract_text_from_pdf(pdf_file) -> str:
    reader = PdfReader(pdf_file)
    full_text = ""
    for page in reader.pages:
        if page.extract_text():
            full_text += page.extract_text() + "\n"
    return full_text.strip()

# 4️⃣ LLM Runner
def run_llm(prompt: str, provider: str = "openai") -> str:
    if provider == "openai":
        import openai
        openai.api_key = OPENAI_API_KEY
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a financial fee analyst AI."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()

    elif provider == "anthropic":
        import anthropic
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        raw = response.content[0].text.strip()
        print("🔍 Claude raw output:\n", raw[:300])
        return raw

    else:
        raise ValueError(f"Unsupported provider: {provider}")

# 5️⃣ Agent Logic
def analyze_document(doc_text: str, provider: str = "openai") -> FeeScenarioAnalysis:
    prompt = build_prompt(doc_text)
    try:
        content = run_llm(prompt, provider=provider)

        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()

        parsed = json.loads(content)
        return FeeScenarioAnalysis(**parsed)

    except Exception as e:
        if provider == "anthropic":
            print("⚠️ Claude failed. Retrying with OpenAI...")
            content = run_llm(prompt, provider="openai")
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()

            print("🔁 Retry content preview:\n", content[:300])
            parsed = json.loads(content)
            return FeeScenarioAnalysis(**parsed)
        else:
            raise e

# 6️⃣ Orchestrator
def process_document(file, provider="openai"):
    text = extract_text_from_pdf(file)
    result = analyze_document(text, provider=provider)

    output = "\U0001F4CA **Fee Scenario Variations**\n\n"
    for scenario in result.scenarios:
        output += f"""
\U0001F9BE **{scenario.participant_type} - {scenario.order_type}**
- Tier: {scenario.volume_tier}
- Fee: {scenario.estimated_fee}
- Rebate: {scenario.rebate}
- Notes: {scenario.notes}

"""
    return output

# 7️⃣ UI Launcher
if __name__ == "__main__":
    print("✅ Multi-LLM Fee Simulator launching...")
    gr.Interface(
        fn=lambda file, provider: process_document(file, provider),
        inputs=[
            gr.File(label="Upload Exchange Fee Schedule (PDF)"),
            gr.Radio(["openai", "anthropic"], label="Choose LLM Provider", value="openai")
        ],
        outputs="text",
        title="Multi-LLM Fee Simulator",
        description="Upload a fee schedule PDF and simulate 3–5 realistic fee/rebate scenarios using GPT-4o or Claude 3."
    ).launch()
