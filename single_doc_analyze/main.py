from typing import BinaryIO
import gradio as gr
import logging
from single_doc_analyze.services.analyzer import DocumentAnalyzer
from single_doc_analyze.services.evaluator import DocumentEvaluator
from single_doc_analyze.services.pdf_service import extract_text_from_pdf
from single_doc_analyze.models.schemas import DocumentAnalysis
from single_doc_analyze.config import settings

logger = logging.getLogger(__name__)

def process_document(file: BinaryIO) -> str:
    """Process uploaded document through analysis and evaluation pipeline.
    
    Args:
        file: A file-like object containing the PDF data
        
    Returns:
        str: Formatted analysis results or error message
    """
    try:
        # Extract text
        text = extract_text_from_pdf(file)
        
        # Initialize services
        analyzer = DocumentAnalyzer()
        evaluator = DocumentEvaluator()
        
        # First pass
        result = analyzer.analyze(text)
        
        # Evaluate
        evaluation = evaluator.evaluate(result)
        
        # Retry if needed
        if not evaluation.is_acceptable:
            logger.info("First analysis attempt failed, retrying with feedback")
            result = analyzer.analyze(text, evaluation.feedback)
        
        # Format output
        return format_analysis_output(result)
        
    except ValueError as e:
        logger.error(f"Document processing error: {str(e)}")
        return f"❌ Error processing document: {str(e)}"
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return f"❌ Unexpected error: {str(e)}"

def format_analysis_output(result: DocumentAnalysis) -> str:
    """Format analysis results for display."""
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

if __name__ == "__main__":
    gr.Interface(
        fn=process_document,
        inputs=gr.File(label="Upload PDF"),
        outputs="text",
        title="One-Shot Document Analyzer",
        description="Upload a document and receive a structured summary with risks and action items."
    ).launch()