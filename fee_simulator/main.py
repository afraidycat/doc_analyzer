import gradio as gr
import logging
from .services.analyzer import FeeAnalyzer
from .services.pdf_service import extract_text_from_pdf
from .config import setup_logging

logger = logging.getLogger(__name__)

def process_document(file, provider="openai"):
    """Process uploaded document through fee analysis pipeline.
    
    Args:
        file: A file-like object containing the PDF data
        provider: The LLM provider to use ("openai" or "anthropic")
        
    Returns:
        str: Formatted fee analysis results or error message
    """
    try:
        # Extract text
        text = extract_text_from_pdf(file)
        
        # Initialize analyzer
        analyzer = FeeAnalyzer()
        
        # Analyze
        result = analyzer.analyze(text, provider=provider)
        
        # Format output
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
        
    except ValueError as e:
        logger.error(f"Document processing error: {str(e)}")
        return f"❌ Error processing document: {str(e)}"
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return f"❌ Unexpected error: {str(e)}"

if __name__ == "__main__":
    # Setup logging
    setup_logging()
    
    logger.info("✅ Multi-LLM Fee Simulator launching...")
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
