import pytest
from single_doc_analyze.services.analyzer import DocumentAnalyzer
from single_doc_analyze.models.schemas import DocumentAnalysis

def test_analyzer_initialization():
    analyzer = DocumentAnalyzer()
    assert analyzer is not None

def test_analyze_with_valid_text():
    analyzer = DocumentAnalyzer()
    test_text = "This is a test document for analysis."
    
    result = analyzer.analyze(test_text)
    
    assert isinstance(result, DocumentAnalysis)
    assert result.summary
    assert isinstance(result.key_topics, list)
    assert isinstance(result.risks_or_issues, list)
    assert isinstance(result.recommended_actions, list)

def test_analyze_with_feedback():
    analyzer = DocumentAnalyzer()
    test_text = "This is a test document for analysis."
    feedback = "Please provide more detailed analysis."
    
    result = analyzer.analyze(test_text, feedback)
    
    assert isinstance(result, DocumentAnalysis)
    assert result.summary
    assert isinstance(result.key_topics, list)
    assert isinstance(result.risks_or_issues, list)
    assert isinstance(result.recommended_actions, list) 