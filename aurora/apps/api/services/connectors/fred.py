from fredapi import Fred
import pandas as pd
import os
from .base import DataConnector

class FredConnector(DataConnector):
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("FRED_API_KEY")
        if self.api_key:
            self.fred = Fred(api_key=self.api_key)
        else:
            self.fred = None

    def fetch_data(self, series_id: str, start_date: str = None, end_date: str = None) -> pd.DataFrame:
        if not self.fred:
            # Fallback or mock data for demo if no API key
            print(f"No FRED API key found. Returning mock data for {series_id}")
            dates = pd.date_range(start="2023-01-01", periods=100, freq="D")
            import numpy as np
            values = np.random.randn(100).cumsum()
            return pd.DataFrame({"timestamp": dates, "value": values}).set_index("timestamp")

        try:
            series = self.fred.get_series(series_id, observation_start=start_date, observation_end=end_date)
            df = pd.DataFrame(series, columns=["value"])
            df.index.name = "timestamp"
            return df
        except Exception as e:
            print(f"Error fetching from FRED: {e}")
            return pd.DataFrame()
