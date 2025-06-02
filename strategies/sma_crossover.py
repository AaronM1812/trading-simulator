import pandas as pd

#this function will generate signals for the sma strategy, in which two smas are created, 10 and 20, when the 10 crosses above the 20, buy, and when it crosses below, sell, there is also logic to check the previous smas to prevent the same signals being generated, ensuring that the signal is only generated when the smas cross, else hold, i.e. the smas are equal
import pandas as pd

def generate_signals(data: pd.DataFrame, short_window: int = 20, long_window: int = 50) -> pd.Series:

    #creating the unpopulated series with the dates as the index, using pandas lib
    signals = pd.Series(index=data.index, dtype="object")

    data['SMA_Short'] = data['Close'].rolling(window=short_window).mean()
    data['SMA_Long'] = data['Close'].rolling(window=long_window).mean()

    previous_position = None

    #iterating through the data and generating the buy and sell signals or none if they are equal or repeated signal
    for i in range(1, len(data)):
        if pd.isna(data['SMA_Short'].iloc[i]) or pd.isna(data['SMA_Long'].iloc[i]):
            continue

        if data['SMA_Short'].iloc[i] > data['SMA_Long'].iloc[i] and data['SMA_Short'].iloc[i - 1] <= data['SMA_Long'].iloc[i - 1]:
            signals.iloc[i] = "buy"
            previous_position = "buy"
        elif data['SMA_Short'].iloc[i] < data['SMA_Long'].iloc[i] and data['SMA_Short'].iloc[i - 1] >= data['SMA_Long'].iloc[i - 1]:
            signals.iloc[i] = "sell"
            previous_position = "sell"
        else:
            signals.iloc[i] = None

    return signals
