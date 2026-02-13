import yfinance as yf
import pandas as pd
from .base import DataConnector

class MarketConnector(DataConnector):
    def fetch_data(self, symbol: str, start_date: str = None, end_date: str = None) -> pd.DataFrame:
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(start=start_date, end=end_date)
            if df.empty:
                return pd.DataFrame()

            # We mostly care about Adjusted Close for returns
            res = df[["Close"]].rename(columns={"Close": "value"})
            res.index.name = "timestamp"
            # Ensure index is timezone naive for DB compatibility if needed
            res.index = res.index.tz_localize(None)
            return res
        except Exception as e:
            print(f"Error fetching from yfinance ({symbol}): {e}")
            return pd.DataFrame()
