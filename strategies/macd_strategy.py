import pandas as pd

def generate_signals(data: pd.DataFrame, short_window=12, long_window=26, signal_window=9):
    data = data.copy()
    
    ema_short = data['Close'].ewm(span=short_window, adjust=False).mean()
    ema_long = data['Close'].ewm(span=long_window, adjust=False).mean()
    
    macd_line = ema_short - ema_long
    signal_line = macd_line.ewm(span=signal_window, adjust=False).mean()

    data['MACD'] = macd_line
    data['Signal'] = signal_line

    signals = [None] * len(data)

    for i in range(1, len(data)):
        macd_prev, macd_curr = data['MACD'].iloc[i - 1], data['MACD'].iloc[i]
        sig_prev, sig_curr = data['Signal'].iloc[i - 1], data['Signal'].iloc[i]

        if pd.isna(macd_prev) or pd.isna(sig_prev) or pd.isna(macd_curr) or pd.isna(sig_curr):
            continue

        if macd_curr > sig_curr and macd_prev <= sig_prev:
            signals[i] = "buy"
        elif macd_curr < sig_curr and macd_prev >= sig_prev:
            signals[i] = "sell"

    return pd.Series(signals, index=data.index)
