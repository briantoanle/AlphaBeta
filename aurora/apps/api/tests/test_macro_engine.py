import pytest
import pandas as pd
import numpy as np
from services.engines.macro_engine import MacroStressEngine

@pytest.mark.parametrize("score, expected_regime", [
    (70.1, "Risk-off"),
    (70.0, "Neutral"),
    (69.9, "Neutral"),
    (50.0, "Neutral"),
    (40.1, "Neutral"),
    (40.0, "Neutral"),
    (39.9, "Risk-on"),
])
def test_detect_regime_boundaries(score, expected_regime):
    engine = MacroStressEngine()
    assert engine.detect_regime(score) == expected_regime

def test_macro_engine():
    engine = MacroStressEngine()

    # Generate some mock data
    dates = pd.date_range(start="2023-01-01", periods=100, freq="D")

    signals = {
        "VIX": pd.DataFrame({"value": np.random.normal(20, 5, 100)}, index=dates),
        "ICSA": pd.DataFrame({"value": np.random.normal(200000, 10000, 100)}, index=dates),
        "recession_trends": pd.DataFrame({"value": np.random.normal(50, 10, 100)}, index=dates),
        "HYG_spread": pd.DataFrame({"value": np.random.normal(4, 0.5, 100)}, index=dates)
    }

    signal_categories = {
        "VIX": "market",
        "ICSA": "labor",
        "recession_trends": "behavioral",
        "HYG_spread": "credit"
    }

    normalized = engine.normalize_signals(signals)
    assert not normalized.empty
    assert "VIX" in normalized.columns

    scores = engine.compute_stress_score(normalized, signal_categories)
    assert not scores.empty
    assert "score" in scores.columns

    latest_score = scores["score"].iloc[-1]
    regime = engine.detect_regime(latest_score)
    assert regime in ["Risk-on", "Neutral", "Risk-off"]

    attribution = engine.get_attribution(normalized.iloc[-1], signal_categories)
    assert len(attribution) > 0

    print(f"Latest Score: {latest_score}")
    print(f"Regime: {regime}")
    print(f"Top Driver: {attribution[0]['signal']}")
    print("MacroStressEngine Test OK")

if __name__ == "__main__":
    test_macro_engine()
