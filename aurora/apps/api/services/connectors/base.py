from abc import ABC, abstractmethod
import pandas as pd

class DataConnector(ABC):
    @abstractmethod
    def fetch_data(self, series_id: str, start_date: str, end_date: str) -> pd.DataFrame:
        pass
