import pytest
from single_doc_analyze.utils.json_utils import clean_json_response, parse_json_response
from single_doc_analyze.models.schemas import DocumentAnalysis

def test_clean_json_response():
    # Test with markdown code block
    input_text = "```json\n{\"key\": \"value\"}\n```"
    expected = "{\"key\": \"value\"}"
    assert clean_json_response(input_text) == expected

    # Test with plain JSON
    input_text = "{\"key\": \"value\"}"
    assert clean_json_response(input_text) == input_text

    # Test with extra whitespace
    input_text = "  {\"key\": \"value\"}  "
    assert clean_json_response(input_text) == "{\"key\": \"value\"}"

def test_parse_json_response():
    # Test with valid JSON
    json_str = """
    {
        "summary": "Test summary",
        "key_topics": ["Topic 1"],
        "risks_or_issues": ["Risk 1"],
        "recommended_actions": ["Action 1"]
    }
    """
    result = parse_json_response(json_str, DocumentAnalysis)
    assert isinstance(result, DocumentAnalysis)
    assert result.summary == "Test summary"
    assert result.key_topics == ["Topic 1"]
    assert result.risks_or_issues == ["Risk 1"]
    assert result.recommended_actions == ["Action 1"]

def test_parse_json_response_with_invalid_json():
    # Test with invalid JSON
    invalid_json = "{invalid json}"
    with pytest.raises(ValueError):
        parse_json_response(invalid_json, DocumentAnalysis)

def test_parse_json_response_with_missing_fields():
    # Test with missing required fields
    incomplete_json = """
    {
        "summary": "Test summary"
    }
    """
    with pytest.raises(ValueError):
        parse_json_response(incomplete_json, DocumentAnalysis) 