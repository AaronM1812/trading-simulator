#library needed for the sma crossover strategy
import pandas as pd

#function which takes in the data and the two sma windows, short and long, used for the SMA strategy and returns the signals of when to buy and sell using this strategy
def generate_signals(data, short_window=20, long_window=50):
    data = data.copy()

    #create the two moving averages
    data['SMA_Short'] = data['Close'].rolling(window=short_window).mean()
    data['SMA_Long'] = data['Close'].rolling(window=long_window).mean()

    #set the signals
    signals = [None] * len(data)

    #setting the previous smas and current used to prevent duplicated signals
    for i in range(1, len(data)):
        short_prev = data['SMA_Short'].iloc[i - 1]
        long_prev = data['SMA_Long'].iloc[i - 1]
        short_now = data['SMA_Short'].iloc[i]
        long_now = data['SMA_Long'].iloc[i]

        #validity check
        if pd.isna(short_prev) or pd.isna(long_prev) or pd.isna(short_now) or pd.isna(long_now):
            continue
        
        #logic to buy and sell if the current signals cross and the previous signal is different
        if short_now > long_now and short_prev <= long_prev:
            signals[i] = "buy"
        elif short_now < long_now and short_prev >= long_prev:
            signals[i] = "sell"
    
    #retunring the signals as a series
    return pd.Series(signals, index=data.index)
