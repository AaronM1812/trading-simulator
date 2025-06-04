import pandas as pd
import numpy as np

def calculate_total_return(equity_curve_list: list) -> float:
    if not equity_curve_list or len(equity_curve_list) < 2:
        return 0.0
    return (equity_curve_list[-1] / equity_curve_list[0]) - 1

def calculate_sharpe_ratio(equity_curve_list: list, risk_free_rate=0.01) -> float:
    if len(equity_curve_list) < 2:
        return 0.0
    equity_curve = pd.Series(equity_curve_list)
    daily_returns = equity_curve.pct_change().dropna()
    excess_returns = daily_returns - (risk_free_rate / 252)
    if excess_returns.std() == 0:
        return 0.0
    return np.sqrt(252) * excess_returns.mean() / excess_returns.std()

def calculate_max_drawdown(equity_curve_list: list) -> float:
    if not equity_curve_list:
        return 0.0
    equity_curve = pd.Series(equity_curve_list)
    running_max = equity_curve.cummax()
    drawdown = (equity_curve - running_max) / running_max
    return drawdown.min()
