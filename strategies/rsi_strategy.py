import pandas as pd
import numpy as np

def generate_signals(data: pd.DataFrame, period: int = 14, overbought: int = 70, oversold: int = 30):
    data = data.copy()
    
    delta = data['Close'].diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)

    avg_gain = pd.Series(gain).rolling(window=period).mean()
    avg_loss = pd.Series(loss).rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    data['RSI'] = rsi

    signals = [None] * len(data)
    for i in range(period, len(data)):
        if data['RSI'].iloc[i] < oversold:
            signals[i] = "buy"
        elif data['RSI'].iloc[i] > overbought:
            signals[i] = "sell"

    return pd.Series(signals, index=data.index)

