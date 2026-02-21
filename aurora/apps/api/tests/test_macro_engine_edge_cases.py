import pandas as pd
import pytest
from services.engines.macro_engine import MacroStressEngine

def test_normalize_signals_empty_input():
    """Test normalize_signals with an empty dictionary."""
    engine = MacroStressEngine()
    normalized = engine.normalize_signals({})

    assert isinstance(normalized, pd.DataFrame)
    assert normalized.empty

def test_normalize_signals_empty_dataframes():
    """Test normalize_signals with a dictionary containing empty DataFrames."""
    engine = MacroStressEngine()
    signals = {
        "EMPTY_SIGNAL": pd.DataFrame(),
        "ANOTHER_EMPTY": pd.DataFrame(columns=["value"])
    }
    normalized = engine.normalize_signals(signals)

    assert isinstance(normalized, pd.DataFrame)
    assert normalized.empty

def test_compute_stress_score_empty_input():
    """Test compute_stress_score with an empty DataFrame."""
    engine = MacroStressEngine()
    scores = engine.compute_stress_score(pd.DataFrame(), {})

    assert isinstance(scores, pd.DataFrame)
    assert scores.empty
