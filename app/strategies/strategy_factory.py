#libraries used for the strategy factory
#type hinting, code clarity
from typing import Dict, Type
#abstract base class for creating interfaces
from abc import ABC, abstractmethod
#pandas for data manipulation
import pandas as pd

#base class for all trading strategies
class Strategy(ABC):
    #abstract method to generate signals, forces all subclasses to implement this method
    @abstractmethod
    #kwargs allows different strats to have different params
    def generate_signals(self, data: pd.DataFrame, **kwargs) -> list:
        #error handling if the method is not implemented
        pass

#simple moving average crossover strategy, inherits from strategy
class SMACrossoverStrategy(Strategy):
    #generating signals for the given price data
    def generate_signals(self, data: pd.DataFrame, **kwargs) -> list:
        short_window = kwargs.get('short_window', 20)
        long_window = kwargs.get('long_window', 50)
        #calculating the moving averages
        data['SMA_short'] = data['Close'].rolling(window=short_window).mean()
        data['SMA_long'] = data['Close'].rolling(window=long_window).mean()
        #list to store the signals
        signals = []
        #loop through the data
        for i in range(len(data)):
            if i < long_window:
                signals.append(None)
                continue
            #if the short moving average is above the long moving average, buy
            if data['SMA_short'].iloc[i] > data['SMA_long'].iloc[i] and \
               data['SMA_short'].iloc[i-1] <= data['SMA_long'].iloc[i-1]:
                signals.append('buy')
            #if the short moving average is below the long moving average, sell
            elif data['SMA_short'].iloc[i] < data['SMA_long'].iloc[i] and \
                 data['SMA_short'].iloc[i-1] >= data['SMA_long'].iloc[i-1]:
                signals.append('sell')
            else:
                signals.append(None)
        #returning the signals
        return signals

#relative strength index strategy
class RSIStrategy(Strategy):
    #generating signals for the given price data
    def generate_signals(self, data: pd.DataFrame, **kwargs) -> list:
        period = kwargs.get('period', 14)
        overbought = kwargs.get('overbought', 70)
        oversold = kwargs.get('oversold', 30)
        #calculating the rsi
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        data['RSI'] = 100 - (100 / (1 + rs))
        #list to store the signals
        signals = []
        #loop through the data
        for i in range(len(data)):
            if i < period:
                signals.append(None)
                continue
            #if the rsi is below the oversold level, buy
            if data['RSI'].iloc[i] < oversold and data['RSI'].iloc[i-1] >= oversold:
                signals.append('buy')
            #if the rsi is above the overbought level, sell
            elif data['RSI'].iloc[i] > overbought and data['RSI'].iloc[i-1] <= overbought:
                signals.append('sell')
            else:
                signals.append(None)
        #returning the signals
        return signals

class MACDStrategy(Strategy):
    #generating signals for the given price data
    def generate_signals(self, data: pd.DataFrame, **kwargs) -> list:
        fast_period = kwargs.get('fast_period', 12)
        slow_period = kwargs.get('slow_period', 26)
        signal_period = kwargs.get('signal_period', 9)
        #calculating the macd
        exp1 = data['Close'].ewm(span=fast_period, adjust=False).mean()
        exp2 = data['Close'].ewm(span=slow_period, adjust=False).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=signal_period, adjust=False).mean()
        #list to store the signals
        signals = []
        #loop through the data
        for i in range(len(data)):
            if i < slow_period:
                signals.append(None)
                continue
            #if the macd is above the signal, buy
            if macd.iloc[i] > signal.iloc[i] and macd.iloc[i-1] <= signal.iloc[i-1]:
                signals.append('buy')
            #if the macd is below the signal, sell
            elif macd.iloc[i] < signal.iloc[i] and macd.iloc[i-1] >= signal.iloc[i-1]:
                signals.append('sell')
            else:
                signals.append(None)
        #returning the signals
        return signals

class BollingerBandsStrategy(Strategy):
    #generating signals for the given price data
    def generate_signals(self, data: pd.DataFrame, **kwargs) -> list:
        window = kwargs.get('window', 20)
        num_std = kwargs.get('num_std', 2)
        #calculating the bollinger bands
        rolling_mean = data['Close'].rolling(window=window).mean()
        rolling_std = data['Close'].rolling(window=window).std()
        upper_band = rolling_mean + num_std * rolling_std
        lower_band = rolling_mean - num_std * rolling_std
        #list to store the signals
        signals = []
        #loop through the data
        for i in range(len(data)):
            if i < window:
                signals.append(None)
                continue
            #if the price is below the lower band, buy
            price = data['Close'].iloc[i]
            if price < lower_band.iloc[i] and data['Close'].iloc[i-1] >= lower_band.iloc[i-1]:
                signals.append('buy')
            #if the price is above the upper band, sell
            elif price > upper_band.iloc[i] and data['Close'].iloc[i-1] <= upper_band.iloc[i-1]:
                signals.append('sell')
            else:
                signals.append(None)
        #returning the signals
        return signals

#strategy registry
STRATEGY_REGISTRY: Dict[str, Type[Strategy]] = {
    "SMA Crossover": SMACrossoverStrategy,
    "RSI Strategy": RSIStrategy,
    "MACD Strategy": MACDStrategy,
    "Bollinger Bands": BollingerBandsStrategy
}

#function to get a strategy instance by name
def get_strategy(strategy_name: str) -> Strategy:
    #error handling if the strategy name is not found
    if strategy_name not in STRATEGY_REGISTRY:
        raise ValueError(f"Strategy '{strategy_name}' not found in registry")
    #returning the strategy instance
    if strategy_name not in STRATEGY_REGISTRY:
        raise ValueError(f"Strategy '{strategy_name}' not found in registry")
    #returning the strategy instance
    return STRATEGY_REGISTRY[strategy_name]()