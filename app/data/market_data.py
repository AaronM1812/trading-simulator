"""
Market data fetching and cleaning utilities.
"""

import yfinance as yf
import pandas as pd
from typing import Union
from datetime import datetime, date

def fetch_market_data(
    ticker: str,
    start_date: Union[str, date, datetime],
    end_date: Union[str, date, datetime]
) -> pd.DataFrame:
    """
    Download historical OHLCV data for a given ticker and date range.
    Returns a cleaned DataFrame indexed by date.
    """
    try:
        # Download data from Yahoo Finance
        data = yf.download(
            ticker,
            start=start_date,
            end=end_date,
            progress=False
        )
        if data.empty:
            raise ValueError(f"No data found for {ticker} in the specified date range")
        # Make sure we have the columns we need
        required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        if not all(col in data.columns for col in required_columns):
            raise ValueError(f"Missing required columns in data for {ticker}")
        # Clean up the DataFrame
        data = data.copy()
        data.index.name = 'Date'
        data = data.dropna()  # Drop any rows with missing values
        return data
    except Exception as e:
        raise ValueError(f"Error fetching data for {ticker}: {str(e)}")

# TODO: Add support for more exotic asset classes (crypto, FX, etc)
def validate_data(df: pd.DataFrame) -> bool:
    """
    Quick check to make sure the DataFrame is valid for backtesting.
    """
    if df.empty:
        return False
    required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    if not all(col in df.columns for col in required_columns):
        return False
    if df.index.name != 'Date':
        return False
    if df.isnull().any().any():
        return False
    return True 