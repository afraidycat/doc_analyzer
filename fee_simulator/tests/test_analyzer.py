import pytest
from ..services.analyzer import FeeAnalyzer
from ..models.schemas import FeeScenarioAnalysis

def test_analyzer_initialization():
    analyzer = FeeAnalyzer()
    assert analyzer is not None

def test_analyze_with_valid_text():
    analyzer = FeeAnalyzer()
    test_text = "Sample fee schedule document."
    
    result = analyzer.analyze(test_text)
    
    assert isinstance(result, FeeScenarioAnalysis)
    assert isinstance(result.scenarios, list)
    assert len(result.scenarios) > 0
    
    scenario = result.scenarios[0]
    assert scenario.participant_type
    assert scenario.volume_tier
    assert scenario.order_type
    assert scenario.estimated_fee
    assert scenario.rebate
    assert scenario.notes

def test_analyze_with_anthropic_fallback():
    analyzer = FeeAnalyzer()
    test_text = "Sample fee schedule document."
    
    # Mock the _run_llm method to simulate Anthropic failure
    def mock_run_llm(prompt, provider):
        if provider == "anthropic":
            raise Exception("Anthropic API error")
        return '{"scenarios": [{"participant_type": "Test", "volume_tier": "Tier 1", "order_type": "Market", "estimated_fee": "$1.00", "rebate": "$0.10", "notes": "Test scenario"}]}'
    
    analyzer._run_llm = mock_run_llm
    
    result = analyzer.analyze(test_text, provider="anthropic")
    
    assert isinstance(result, FeeScenarioAnalysis)
    assert len(result.scenarios) == 1
    assert result.scenarios[0].participant_type == "Test" 