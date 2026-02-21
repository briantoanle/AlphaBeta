import pytest
from pydantic import ValidationError
from models.schemas import HoldingBase, PortfolioBase

def test_holding_validation():
    # Valid holding
    h = HoldingBase(symbol="AAPL", weight=0.5)
    assert h.symbol == "AAPL"
    assert h.weight == 0.5

    # Negative weight
    with pytest.raises(ValidationError):
        HoldingBase(symbol="AAPL", weight=-0.1)

    # Weight > 1.0
    with pytest.raises(ValidationError):
        HoldingBase(symbol="AAPL", weight=1.1)

    # Infinity weight
    with pytest.raises(ValidationError):
        HoldingBase(symbol="AAPL", weight=float('inf'))

    # NaN weight
    with pytest.raises(ValidationError):
        HoldingBase(symbol="AAPL", weight=float('nan'))

def test_portfolio_validation():
    # Valid portfolio
    holdings = [HoldingBase(symbol="AAPL", weight=1.0)]
    p = PortfolioBase(name="My Portfolio", holdings=holdings)
    assert p.name == "My Portfolio"
    assert len(p.holdings) == 1

    # Negative riskTolerance
    with pytest.raises(ValidationError):
        PortfolioBase(name="Test", holdings=holdings, riskTolerance=-1.0)

    # Zero horizon
    with pytest.raises(ValidationError):
        PortfolioBase(name="Test", holdings=holdings, horizon=0)

    # Negative horizon
    with pytest.raises(ValidationError):
        PortfolioBase(name="Test", holdings=holdings, horizon=-5)
