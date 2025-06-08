#libraries needed to fetch the data
import yfinance as yf
import pandas as pd

#function which fetches the data using the stock ticker and dates
def fetch_data(ticker: str, start: str, end: str) -> pd.DataFrame:
    #downloading the data from yahoo finance
    df = yf.download(ticker, start=start, end=end)
    #fill in any missing values
    df.ffill(inplace=True)
    #returning the dataframe
    return df
