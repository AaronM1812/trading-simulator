#library needed for the MACD strategy
import pandas as pd

#function which generates the buy and sell signals for the MACD strategy using the data, windows and a signal window
def generate_signals(data: pd.DataFrame, short_window=12, long_window=26, signal_window=9):
    data = data.copy()
    
    #the short and long exponentional averages
    ema_short = data['Close'].ewm(span=short_window, adjust=False).mean()
    ema_long = data['Close'].ewm(span=long_window, adjust=False).mean()
    
    #the macd line and signal line generated from the macdline
    macd_line = ema_short - ema_long
    signal_line = macd_line.ewm(span=signal_window, adjust=False).mean()

    data['MACD'] = macd_line
    data['Signal'] = signal_line

    signals = [None] * len(data)

    #the logic to buy and sell using the previous and current MACD and signals
    for i in range(1, len(data)):
        macd_prev, macd_curr = data['MACD'].iloc[i - 1], data['MACD'].iloc[i]
        sig_prev, sig_curr = data['Signal'].iloc[i - 1], data['Signal'].iloc[i]

        if pd.isna(macd_prev) or pd.isna(sig_prev) or pd.isna(macd_curr) or pd.isna(sig_curr):
            continue

        if macd_curr > sig_curr and macd_prev <= sig_prev:
            signals[i] = "buy"
        elif macd_curr < sig_curr and macd_prev >= sig_prev:
            signals[i] = "sell"

    #returning a series of signals
    return pd.Series(signals, index=data.index)
