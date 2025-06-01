import yfinance as yf
import pandas as pd

#function that will return the data we need from yahoo finance using the args
def fetch_data(ticker: str, start: str, end: str) -> pd.DataFrame:
    df = yf.download(ticker, start=start, end=end)
    #forward-fill missing values
    df.ffill(inplace=True)
    return df