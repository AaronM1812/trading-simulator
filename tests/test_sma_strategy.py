import pandas as pd
import numpy as np
from app.strategies.strategy_factory import SMACrossoverStrategy

def test_sma_crossover_signals():
    # Generate some fake price data
    dates = pd.date_range(start="2023-01-01", periods=50, freq="D")
    prices = np.linspace(100, 120, 50)
    df = pd.DataFrame({"Close": prices}, index=dates)
    strategy = SMACrossoverStrategy()
    signals = strategy.generate_signals(df, short_window=5, long_window=20)
    # Should return a list of the same length as the data
    assert isinstance(signals, list)
    assert len(signals) == len(df)
    # TODO: Add more tests for actual signal logic if needed 