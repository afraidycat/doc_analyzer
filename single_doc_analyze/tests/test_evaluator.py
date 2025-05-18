import pytest
from single_doc_analyze.services.evaluator import DocumentEvaluator
from single_doc_analyze.models.schemas import DocumentAnalysis, EvaluationResult

def test_evaluator_initialization():
    evaluator = DocumentEvaluator()
    assert evaluator is not None

def test_evaluate_with_valid_analysis():
    evaluator = DocumentEvaluator()
    analysis = DocumentAnalysis(
        summary="Test summary",
        key_topics=["Topic 1", "Topic 2"],
        risks_or_issues=["Risk 1"],
        recommended_actions=["Action 1"]
    )
    
    result = evaluator.evaluate(analysis)
    
    assert isinstance(result, EvaluationResult)
    assert isinstance(result.is_acceptable, bool)
    assert isinstance(result.feedback, str)

def test_evaluate_with_minimal_analysis():
    evaluator = DocumentEvaluator()
    analysis = DocumentAnalysis(
        summary="Minimal summary",
        key_topics=[],
        risks_or_issues=[],
        recommended_actions=[]
    )
    
    result = evaluator.evaluate(analysis)
    
    assert isinstance(result, EvaluationResult)
    assert isinstance(result.is_acceptable, bool)
    assert isinstance(result.feedback, str) 