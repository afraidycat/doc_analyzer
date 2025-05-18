import pytest
from io import BytesIO
from single_doc_analyze.services.pdf_service import extract_text_from_pdf

def test_extract_text_from_pdf_with_valid_pdf():
    # Create a simple PDF file in memory
    pdf_content = b"%PDF-1.4\n1 0 obj\n<<>>\nendobj\ntrailer\n<<>>\n%%EOF"
    pdf_file = BytesIO(pdf_content)
    
    with pytest.raises(ValueError):
        # This should raise an error since it's not a valid PDF
        extract_text_from_pdf(pdf_file)

def test_extract_text_from_pdf_with_invalid_file():
    # Create an invalid file
    invalid_file = BytesIO(b"Not a PDF file")
    
    with pytest.raises(ValueError):
        extract_text_from_pdf(invalid_file)

def test_extract_text_from_pdf_with_empty_file():
    # Create an empty file
    empty_file = BytesIO(b"")
    
    with pytest.raises(ValueError):
        extract_text_from_pdf(empty_file) 