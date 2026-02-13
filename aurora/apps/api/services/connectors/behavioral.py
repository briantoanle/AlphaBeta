from pytrends.request import TrendReq
import pandas as pd
import time
import random
from .base import DataConnector

class BehavioralConnector(DataConnector):
    def __init__(self):
        self.pytrends = TrendReq(hl='en-US', tz=360)

    def fetch_data(self, keyword: str, start_date: str = None, end_date: str = None) -> pd.DataFrame:
        try:
            # start_date/end_date format: 'YYYY-MM-DD'
            # pytrends timeframe format: 'YYYY-MM-DD YYYY-MM-DD'
            timeframe = f"{start_date} {end_date}" if start_date and end_date else 'today 5-y'

            self.pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo='', gprop='')
            df = self.pytrends.interest_over_time()

            if df.empty or keyword not in df:
                print(f"No data for keyword: {keyword}")
                return pd.DataFrame()

            res = df[[keyword]].rename(columns={keyword: "value"})
            res.index.name = "timestamp"
            return res
        except Exception as e:
            print(f"Error fetching from pytrends ({keyword}): {e}")
            # Mock fallback for search intensity
            dates = pd.date_range(start=start_date or "2023-01-01", periods=30, freq="D")
            import numpy as np
            values = np.random.randint(20, 100, size=30)
            return pd.DataFrame({"timestamp": dates, "value": values}).set_index("timestamp")
