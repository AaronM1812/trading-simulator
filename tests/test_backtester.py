import pandas as pd
import numpy as np
from app.core.backtester import Backtester

def test_backtester_runs():
    # Create some fake price data
    dates = pd.date_range(start="2023-01-01", periods=30, freq="D")
    prices = np.linspace(100, 110, 30)
    df = pd.DataFrame({"Close": prices}, index=dates)
    # Simple signals: buy on even days, sell on odd days
    signals = ["buy" if i % 2 == 0 else "sell" for i in range(30)]
    backtester = Backtester(df, signals)
    equity_curve = backtester.run()
    # Should return a DataFrame with the same length as input
    assert not equity_curve.empty
    assert len(equity_curve) == len(df)
    # TODO: Add more detailed tests for PnL, trade log, etc. 