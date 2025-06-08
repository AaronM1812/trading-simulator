#the libraries needed to carry out the RSI strategy
import pandas as pd
import numpy as np

#the function to generate the buy and sell signals for the RSI strategy using the data, period, and thresholds
def generate_signals(data: pd.DataFrame, period: int = 14, overbought: int = 70, oversold: int = 30):
    data = data.copy()

    #setting the closing prices and the deltas
    close_prices = data["Close"].squeeze().tolist()
    deltas = [close_prices[i] - close_prices[i-1] for i in range(1, len(close_prices))]

    #getting the gains and losses used in the formula
    gains = [max(delta, 0) for delta in deltas]
    losses = [abs(min(delta, 0)) for delta in deltas]

    #lists which will carry the average of the gains and losses
    avg_gains = []
    avg_losses = []

    #the first average which is a simple mean
    first_avg_gain = sum(gains[:period]) / period
    first_avg_loss = sum(losses[:period]) / period

    #appending this to the lists
    avg_gains.append(first_avg_gain)
    avg_losses.append(first_avg_loss)

    #rest use smoothing
    for i in range(period, len(gains)):
        #setting the previous gains and losses
        prev_avg_gain = avg_gains[-1]
        prev_avg_loss = avg_losses[-1]

        #working out the new gains and losses using this
        new_avg_gain = (prev_avg_gain * (period - 1) + gains[i]) / period
        new_avg_loss = (prev_avg_loss * (period - 1) + losses[i]) / period

        #appeneding this to the lists
        avg_gains.append(new_avg_gain)
        avg_losses.append(new_avg_loss)

    #pad for alignment
    rsis = [None] * (period)

    #iterating through the average gains and losses tuple
    for ag, al in zip(avg_gains, avg_losses):
        #using the RSI formula
        rs = ag / al if al != 0 else 0
        rsi = 100 - (100 / (1 + rs))
        rsis.append(rsi)

    signals = [None] * len(close_prices)
    #logic to buy and sell depending on RSI value and thresholds
    for i in range(len(rsis)):
        if rsis[i] is None:
            continue
        if rsis[i] < oversold:
            signals[i] = "buy"
        elif rsis[i] > overbought:
            signals[i] = "sell"

    #returning the signals
    return signals
