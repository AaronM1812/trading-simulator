import pandas as pd

#function which will implement the sma strategy and generate the signals, this will then be added as a new column in the datafrane
def generate_signals(data):
    #takes in the data frame which must contain the close column

    df = data.copy()

    #simple 10/20-day moving average crossover
    df['SMA10'] = df['Close'].rolling(window=10).mean()
    df['SMA20'] = df['Close'].rolling(window=20).mean()

    #logic to generate the signals based on the sma
    df['Signal'] = 'hold'
    df.loc[df['SMA10'] > df['SMA20'], 'Signal'] = 'buy'
    df.loc[df['SMA10'] < df['SMA20'], 'Signal'] = 'sell'

    return df
