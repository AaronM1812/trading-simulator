import pandas as pd
import numpy as np

def generate_signals(data: pd.DataFrame, period: int = 14, overbought: int = 70, oversold: int = 30):
    data = data.copy()

    close_prices = data["Close"].squeeze().tolist()
    deltas = [close_prices[i] - close_prices[i-1] for i in range(1, len(close_prices))]

    gains = [max(delta, 0) for delta in deltas]
    losses = [abs(min(delta, 0)) for delta in deltas]

    avg_gains = []
    avg_losses = []

    # First average (simple mean)
    first_avg_gain = sum(gains[:period]) / period
    first_avg_loss = sum(losses[:period]) / period

    avg_gains.append(first_avg_gain)
    avg_losses.append(first_avg_loss)

    # Rest use smoothing
    for i in range(period, len(gains)):
        prev_avg_gain = avg_gains[-1]
        prev_avg_loss = avg_losses[-1]

        new_avg_gain = (prev_avg_gain * (period - 1) + gains[i]) / period
        new_avg_loss = (prev_avg_loss * (period - 1) + losses[i]) / period

        avg_gains.append(new_avg_gain)
        avg_losses.append(new_avg_loss)

    rsis = [None] * (period)  # pad for alignment
    for ag, al in zip(avg_gains, avg_losses):
        rs = ag / al if al != 0 else 0
        rsi = 100 - (100 / (1 + rs))
        rsis.append(rsi)

    signals = [None] * len(close_prices)
    for i in range(len(rsis)):
        if rsis[i] is None:
            continue
        if rsis[i] < oversold:
            signals[i] = "buy"
        elif rsis[i] > overbought:
            signals[i] = "sell"

    return signals
