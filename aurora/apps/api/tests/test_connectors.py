from services.connectors.fred import FredConnector
from services.connectors.market import MarketConnector
from services.connectors.behavioral import BehavioralConnector
import pandas as pd

def test_market():
    print("Testing MarketConnector (SPY)...")
    market = MarketConnector()
    df = market.fetch_data("SPY", start_date="2024-01-01", end_date="2024-01-10")
    print(df.head())
    assert not df.empty
    print("MarketConnector OK")

def test_fred_mock():
    print("Testing FredConnector (Mock)...")
    fred = FredConnector(api_key=None)
    df = fred.fetch_data("ICSA")
    print(df.head())
    assert not df.empty
    print("FredConnector Mock OK")

def test_behavioral():
    print("Testing BehavioralConnector (recession)...")
    behavioral = BehavioralConnector()
    df = behavioral.fetch_data("recession", start_date="2024-01-01", end_date="2024-01-30")
    print(df.head())
    assert not df.empty
    print("BehavioralConnector OK")

if __name__ == "__main__":
    try:
        test_market()
    except Exception as e:
        print(f"Market test failed: {e}")

    try:
        test_fred_mock()
    except Exception as e:
        print(f"Fred test failed: {e}")

    try:
        test_behavioral()
    except Exception as e:
        print(f"Behavioral test failed: {e}")
