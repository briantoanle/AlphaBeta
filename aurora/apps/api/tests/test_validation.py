import pytest
from pydantic import ValidationError
from models.schemas import PortfolioBase

def test_portfolio_base_validation():
    # Valid data
    valid_data = {
        "name": "My Portfolio",
        "holdings": [{"symbol": "SPY", "weight": 1.0}],
        "riskTolerance": 5.0,
        "horizon": 10
    }
    p = PortfolioBase(**valid_data)
    assert p.riskTolerance == 5.0
    assert p.horizon == 10

    # Invalid riskTolerance (too high)
    with pytest.raises(ValidationError):
        PortfolioBase(**{**valid_data, "riskTolerance": 11.0})

    # Invalid riskTolerance (too low)
    with pytest.raises(ValidationError):
        PortfolioBase(**{**valid_data, "riskTolerance": -1.0})

    # Invalid horizon (too low)
    with pytest.raises(ValidationError):
        PortfolioBase(**{**valid_data, "horizon": 0})

    # Invalid horizon (too high)
    with pytest.raises(ValidationError):
        PortfolioBase(**{**valid_data, "horizon": 101})
