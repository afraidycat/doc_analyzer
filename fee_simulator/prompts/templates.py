def build_prompt(doc_text: str) -> str:
    """Build the prompt for fee analysis."""
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