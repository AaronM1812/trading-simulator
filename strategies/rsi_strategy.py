import pandas as pd
import numpy as np

#this function will generate signals to buy and sell or hold based on the rsi strategy, the rsi is first calculated, then if the rsi is above 70 then it is overbought and a sell signal will be generated, else if its below 30 then its oversold and a buy signal will be generated, else if its between this range the hold signal will be generated, the rsi indicated the strength of the price, and is calculated using the rsi formula
def generate_signals(data):

    #create a copy of the dataframe
    df = data.copy()

    #get the gain and loss using the closing prices
    delta = df['Close'].diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)

    #find the average gain and loss in a 14 day window
    avg_gain = pd.Series(gain).rolling(window=14).mean()
    avg_loss = pd.Series(loss).rolling(window=14).mean()

    #divide the two and using the rsi formula to find out the rsi
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    df['RSI'] = rsi

    #logic here to generate the signals, hold is between 70 and 30, sell if above 70, buy if below 30
    df['Signal'] = 'hold'
    df.loc[df['RSI'] < 30, 'Signal'] = 'buy'
    df.loc[df['RSI'] > 70, 'Signal'] = 'sell'

    return df
