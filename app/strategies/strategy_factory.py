"""
Strategy factory and base classes for trading strategies.
"""

from typing import Dict, Type
from abc import ABC, abstractmethod
import pandas as pd

class Strategy(ABC):
    """
    Base class for all trading strategies. Each strategy must implement generate_signals.
    """
    @abstractmethod
    def generate_signals(self, data: pd.DataFrame, **kwargs) -> list:
        """
        Generate buy/sell/hold signals for the given price data.
        """
        pass

class SMACrossoverStrategy(Strategy):
    """
    Simple Moving Average Crossover strategy.
    Buys when short MA crosses above long MA, sells when it crosses below.
    """
    def generate_signals(self, data: pd.DataFrame, **kwargs) -> list:
        short_window = kwargs.get('short_window', 20)
        long_window = kwargs.get('long_window', 50)
        # Calculate moving averages
        data['SMA_short'] = data['Close'].rolling(window=short_window).mean()
        data['SMA_long'] = data['Close'].rolling(window=long_window).mean()
        signals = []
        for i in range(len(data)):
            if i < long_window:
                signals.append(None)
                continue
            if data['SMA_short'].iloc[i] > data['SMA_long'].iloc[i] and \
               data['SMA_short'].iloc[i-1] <= data['SMA_long'].iloc[i-1]:
                signals.append('buy')
            elif data['SMA_short'].iloc[i] < data['SMA_long'].iloc[i] and \
                 data['SMA_short'].iloc[i-1] >= data['SMA_long'].iloc[i-1]:
                signals.append('sell')
            else:
                signals.append(None)
        return signals

class RSIStrategy(Strategy):
    """
    Relative Strength Index (RSI) strategy.
    Buys when RSI crosses below oversold, sells when it crosses above overbought.
    """
    def generate_signals(self, data: pd.DataFrame, **kwargs) -> list:
        period = kwargs.get('period', 14)
        overbought = kwargs.get('overbought', 70)
        oversold = kwargs.get('oversold', 30)
        # Calculate RSI
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        data['RSI'] = 100 - (100 / (1 + rs))
        signals = []
        for i in range(len(data)):
            if i < period:
                signals.append(None)
                continue
            if data['RSI'].iloc[i] < oversold and data['RSI'].iloc[i-1] >= oversold:
                signals.append('buy')
            elif data['RSI'].iloc[i] > overbought and data['RSI'].iloc[i-1] <= overbought:
                signals.append('sell')
            else:
                signals.append(None)
        return signals

class MACDStrategy(Strategy):
    """
    Moving Average Convergence Divergence (MACD) strategy.
    Buys when MACD crosses above signal, sells when it crosses below.
    """
    def generate_signals(self, data: pd.DataFrame, **kwargs) -> list:
        fast_period = kwargs.get('fast_period', 12)
        slow_period = kwargs.get('slow_period', 26)
        signal_period = kwargs.get('signal_period', 9)
        # Calculate MACD
        exp1 = data['Close'].ewm(span=fast_period, adjust=False).mean()
        exp2 = data['Close'].ewm(span=slow_period, adjust=False).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=signal_period, adjust=False).mean()
        signals = []
        for i in range(len(data)):
            if i < slow_period:
                signals.append(None)
                continue
            if macd.iloc[i] > signal.iloc[i] and macd.iloc[i-1] <= signal.iloc[i-1]:
                signals.append('buy')
            elif macd.iloc[i] < signal.iloc[i] and macd.iloc[i-1] >= signal.iloc[i-1]:
                signals.append('sell')
            else:
                signals.append(None)
        return signals

class BollingerBandsStrategy(Strategy):
    """
    Bollinger Bands strategy.
    Buys when price crosses above the lower band, sells when it crosses below the upper band.
    """
    def generate_signals(self, data: pd.DataFrame, **kwargs) -> list:
        window = kwargs.get('window', 20)
        num_std = kwargs.get('num_std', 2)
        # Classic Bollinger Bands logic: buy the dip, sell the rip
        rolling_mean = data['Close'].rolling(window=window).mean()
        rolling_std = data['Close'].rolling(window=window).std()
        upper_band = rolling_mean + num_std * rolling_std
        lower_band = rolling_mean - num_std * rolling_std
        signals = []
        for i in range(len(data)):
            if i < window:
                signals.append(None)
                continue
            price = data['Close'].iloc[i]
            if price < lower_band.iloc[i] and data['Close'].iloc[i-1] >= lower_band.iloc[i-1]:
                signals.append('buy')
            elif price > upper_band.iloc[i] and data['Close'].iloc[i-1] <= upper_band.iloc[i-1]:
                signals.append('sell')
            else:
                signals.append(None)
        return signals

# Strategy registry
STRATEGY_REGISTRY: Dict[str, Type[Strategy]] = {
    "SMA Crossover": SMACrossoverStrategy,
    "RSI Strategy": RSIStrategy,
    "MACD Strategy": MACDStrategy,
    "Bollinger Bands": BollingerBandsStrategy
}

def get_strategy(strategy_name: str) -> Strategy:
    """
    Get a strategy instance by name.
    
    Args:
        strategy_name: Name of the strategy to instantiate
    
    Returns:
        Strategy: Instance of the requested strategy
    
    Raises:
        ValueError: If strategy name is not found in registry
    """
    if strategy_name not in STRATEGY_REGISTRY:
        raise ValueError(f"Strategy '{strategy_name}' not found in registry")
    
    return STRATEGY_REGISTRY[strategy_name]()

# TODO: Add more strategies (momentum, mean reversion, etc) 