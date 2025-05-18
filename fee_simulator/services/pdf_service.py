import logging
from typing import BinaryIO
from pypdf import PdfReader

logger = logging.getLogger(__name__)

def extract_text_from_pdf(pdf_file: BinaryIO) -> str:
    """Extract text content from a PDF file.
    
    Args:
        pdf_file: A file-like object containing the PDF data
        
    Returns:
        str: The extracted text content
        
    Raises:
        ValueError: If the PDF cannot be read or text cannot be extracted
    """
    try:
        reader = PdfReader(pdf_file)
        full_text = ""
        for page in reader.pages:
            if page.extract_text():
                full_text += page.extract_text() + "\n"
        return full_text.strip()
    except Exception as e:
        logger.error(f"Failed to extract text from PDF: {str(e)}")
        raise ValueError(f"Failed to extract text from PDF: {str(e)}") 