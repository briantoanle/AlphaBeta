from services.engines.portfolio_engine import PortfolioRiskEngine

def test_portfolio_engine():
    engine = PortfolioRiskEngine()

    holdings = [
        {"symbol": "SPY", "weight": 0.6},
        {"symbol": "TLT", "weight": 0.3},
        {"symbol": "GLD", "weight": 0.1}
    ]

    exposure = engine.compute_exposure(holdings)
    assert "equity" in exposure
    print(f"Exposure: {exposure}")

    stress = engine.run_stress_test(holdings, "recession")
    assert "expected_return" in stress
    print(f"Recession stress test: {stress}")

    fragility = engine.compute_fragility_score(holdings)
    assert 0 <= fragility <= 100
    print(f"Fragility Score: {fragility}")

    mc = engine.monte_carlo_drawdown(holdings, iterations=100)
    assert "worst_case_drawdown" in mc
    print(f"Monte Carlo: {mc}")

    print("PortfolioRiskEngine Test OK")

if __name__ == "__main__":
    test_portfolio_engine()
