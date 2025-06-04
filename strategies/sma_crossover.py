import pandas as pd

def generate_signals(data, short_window=20, long_window=50):
    data = data.copy()
    data['SMA_Short'] = data['Close'].rolling(window=short_window).mean()
    data['SMA_Long'] = data['Close'].rolling(window=long_window).mean()

    signals = [None] * len(data)

    for i in range(1, len(data)):
        short_prev = data['SMA_Short'].iloc[i - 1]
        long_prev = data['SMA_Long'].iloc[i - 1]
        short_now = data['SMA_Short'].iloc[i]
        long_now = data['SMA_Long'].iloc[i]

        if pd.isna(short_prev) or pd.isna(long_prev) or pd.isna(short_now) or pd.isna(long_now):
            continue

        if short_now > long_now and short_prev <= long_prev:
            signals[i] = "buy"
        elif short_now < long_now and short_prev >= long_prev:
            signals[i] = "sell"
    
    return pd.Series(signals, index=data.index)
