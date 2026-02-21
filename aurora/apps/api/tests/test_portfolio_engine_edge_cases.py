from services.engines.portfolio_engine import PortfolioRiskEngine
import pytest

def test_compute_exposure_unknown_symbol():
    """
    Test that a symbol not in factor_betas falls back to SPY default.
    """
    engine = PortfolioRiskEngine()

    # "UNKNOWN" is not in the engine's factor_betas
    holdings = [
        {"symbol": "UNKNOWN", "weight": 1.0}
    ]

    exposure = engine.compute_exposure(holdings)

    # SPY default betas are {"equity": 1.0, "rates": -0.2, "vol": -0.5}
    assert exposure["equity"] == 1.0
    assert exposure["rates"] == -0.2
    assert exposure["vol"] == -0.5

def test_compute_exposure_mixed_unknown_symbol():
    """
    Test a mix of known and unknown symbols.
    """
    engine = PortfolioRiskEngine()

    # SPY: {"equity": 1.0, "rates": -0.2, "vol": -0.5}
    # CASH: {"equity": 0.0, "rates": 0.0, "vol": 0.0}
    # UNKNOWN (falls back to SPY): {"equity": 1.0, "rates": -0.2, "vol": -0.5}

    holdings = [
        {"symbol": "CASH", "weight": 0.5},
        {"symbol": "UNKNOWN", "weight": 0.5}
    ]

    exposure = engine.compute_exposure(holdings)

    # Expected: 0.5 * 0.0 + 0.5 * 1.0 = 0.5
    assert pytest.approx(exposure["equity"]) == 0.5
    # Expected: 0.5 * 0.0 + 0.5 * -0.2 = -0.1
    assert pytest.approx(exposure["rates"]) == -0.1
    # Expected: 0.5 * 0.0 + 0.5 * -0.5 = -0.25
    assert pytest.approx(exposure["vol"]) == -0.25
