#libraries used for fetching market data
import yfinance as yf
import pandas as pd
#union used for type hinting, so it can accept either a string, date or datetime for instance
from typing import Union
from datetime import datetime, date

#function to fetch market data from yahoo finance
def fetch_market_data(
    ticker: str,
    #here is the example of type hinting
    start_date: Union[str, date, datetime],
    end_date: Union[str, date, datetime]
) -> pd.DataFrame:

    #error handlign using try except block
    try:
        #download the data from yahoo finance
        data = yf.download(
            ticker,
            start=start_date,
            end=end_date,
            progress=False
        )
        #error handling if no data is found
        if data.empty:
            raise ValueError(f"No data found for {ticker} in the specified date range")
        #error handling if the required columns are not found
        required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        if not all(col in data.columns for col in required_columns):
            #error message if the required columns are not found
            raise ValueError(f"Missing required columns in data for {ticker}")
        #cleaning up the dataframe
        data = data.copy()
        data.index.name = 'Date'
        #dropping any rows with missing values
        data = data.dropna()
        #returning the cleaned dataframe
        return data
    #catching any errors and raising a value error with the error message
    except Exception as e:
        raise ValueError(f"Error fetching data for {ticker}: {str(e)}")

#function to validate the data
def validate_data(df: pd.DataFrame) -> bool:

    #error handling if the dataframe is empty
    if df.empty:
        return False
    #error handling if the required columns are not found
    required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    if not all(col in df.columns for col in required_columns):
        return False
    #error handling if the index name is not 'Date'
    if df.index.name != 'Date':
        return False
    #error handling if there are any missing values
    if df.isnull().any().any():
        return False
    #returning true if the data is valid
    return True 