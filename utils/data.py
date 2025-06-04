import yfinance as yf
import pandas as pd

def fetch_data(ticker: str, start: str, end: str) -> pd.DataFrame:
    df = yf.download(ticker, start=start, end=end)
    df.ffill(inplace=True)
    return df
