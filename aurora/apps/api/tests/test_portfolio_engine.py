import pytest
from services.engines.portfolio_engine import PortfolioRiskEngine

def test_portfolio_engine_basic():
    engine = PortfolioRiskEngine()

    holdings = [
        {"symbol": "SPY", "weight": 0.6},
        {"symbol": "TLT", "weight": 0.3},
        {"symbol": "GLD", "weight": 0.1}
    ]

    exposure = engine.compute_exposure(holdings)
    assert "equity" in exposure

    stress = engine.run_stress_test(holdings, "recession")
    assert "expected_return" in stress

    fragility = engine.compute_fragility_score(holdings)
    assert 0 <= fragility <= 100

    mc = engine.monte_carlo_drawdown(holdings, iterations=100)
    assert "worst_case_drawdown" in mc

def test_compute_fragility_score_empty():
    """Test fragility score with empty holdings list."""
    engine = PortfolioRiskEngine()
    assert engine.compute_fragility_score([]) == 0.0

def test_compute_fragility_score_single_holding():
    """Test fragility score with a single highly concentrated holding."""
    engine = PortfolioRiskEngine()
    holdings = [{"symbol": "SPY", "weight": 1.0}]
    # HHI = 1.0, avg_beta = 1.0 (equity) + 0.2 (rates) + 0.5 (vol) = 1.7
    # Score = (1.0 * 50) + (1.7 / 2.0 * 50) = 50 + 42.5 = 92.5
    assert engine.compute_fragility_score(holdings) == pytest.approx(92.5)

def test_compute_fragility_score_diversified():
    """Test fragility score with a diversified portfolio."""
    engine = PortfolioRiskEngine()
    holdings = [
        {"symbol": "SPY", "weight": 0.2},
        {"symbol": "TLT", "weight": 0.2},
        {"symbol": "GLD", "weight": 0.2},
        {"symbol": "USO", "weight": 0.2},
        {"symbol": "HYG", "weight": 0.2}
    ]
    # HHI = 0.2, avg_beta = 0.78
    # Score = (0.2 * 50) + (0.78 / 2.0 * 50) = 10 + 19.5 = 29.5
    assert engine.compute_fragility_score(holdings) == pytest.approx(29.5)

def test_compute_fragility_score_invalid_weights():
    """Test fragility score with missing weight keys should raise KeyError."""
    engine = PortfolioRiskEngine()
    holdings = [{"symbol": "SPY"}]
    with pytest.raises(KeyError):
        engine.compute_fragility_score(holdings)
