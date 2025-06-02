import pandas as pd
import numpy as np

#this function will generate signals to buy and sell or hold based on the rsi strategy, the rsi is first calculated, then if the rsi is above 70 then it is overbought and a sell signal will be generated, else if its below 30 then its oversold and a buy signal will be generated, else if its between this range the hold signal will be generated, the rsi indicated the strength of the price, and is calculated using the rsi formula
def generate_signals(data: pd.DataFrame, period: int = 14, overbought: int = 70, oversold: int = 30) -> pd.Series:
    """
    RSI Strategy:
    - Buy when RSI drops below 30 (oversold)
    - Sell when RSI rises above 70 (overbought)
    """
    signals = pd.Series(index=data.index, dtype="object")

    delta = data['Close'].diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)

    avg_gain = pd.Series(gain).rolling(window=period).mean()
    avg_loss = pd.Series(loss).rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    data['RSI'] = rsi

    #iterating through the data and generating the buy and sell signals or none if RSI is within 70 and 30 or repeated signal
    for i in range(period, len(data)):
        if data['RSI'].iloc[i] < oversold:
            signals.iloc[i] = "buy"
        elif data['RSI'].iloc[i] > overbought:
            signals.iloc[i] = "sell"
        else:
            signals.iloc[i] = None

    return signals

