"""
Performance metrics calculation module.
Provides functions for calculating various trading performance metrics.
"""

import numpy as np
import pandas as pd
from typing import List, Union

def calculate_total_return(equity_curve: Union[List[float], pd.Series]) -> float:
    """
    Calculate the total return of the strategy.
    
    Args:
        equity_curve: List or Series of equity values
    
    Returns:
        float: Total return as a percentage
    """
    if isinstance(equity_curve, list):
        equity_curve = pd.Series(equity_curve)
    
    initial_value = equity_curve.iloc[0]
    final_value = equity_curve.iloc[-1]
    
    return ((final_value - initial_value) / initial_value) * 100

def calculate_sharpe_ratio(returns: Union[List[float], pd.Series], risk_free_rate: float = 0.02) -> float:
    """
    Calculate the Sharpe ratio of the strategy.
    
    Args:
        returns: List or Series of returns
        risk_free_rate: Annual risk-free rate (default: 2%)
    
    Returns:
        float: Sharpe ratio
    """
    if isinstance(returns, list):
        returns = pd.Series(returns)
    
    # Convert returns to annual
    annual_returns = returns.mean() * 252
    annual_volatility = returns.std() * np.sqrt(252)
    
    if annual_volatility == 0:
        return 0.0
    
    return (annual_returns - risk_free_rate) / annual_volatility

def calculate_max_drawdown(equity_curve: Union[List[float], pd.Series]) -> float:
    """
    Calculate the maximum drawdown of the strategy.
    
    Args:
        equity_curve: List or Series of equity values
    
    Returns:
        float: Maximum drawdown as a percentage
    """
    if isinstance(equity_curve, list):
        equity_curve = pd.Series(equity_curve)
    
    # Calculate running maximum
    running_max = equity_curve.expanding().max()
    
    # Calculate drawdowns
    drawdowns = (equity_curve - running_max) / running_max * 100
    
    return abs(drawdowns.min())

def calculate_cagr(equity_curve: Union[List[float], pd.Series], years: float) -> float:
    """
    Calculate the Compound Annual Growth Rate (CAGR).
    
    Args:
        equity_curve: List or Series of equity values
        years: Number of years in the backtest period
    
    Returns:
        float: CAGR as a percentage
    """
    if isinstance(equity_curve, list):
        equity_curve = pd.Series(equity_curve)
    
    initial_value = equity_curve.iloc[0]
    final_value = equity_curve.iloc[-1]
    
    return ((final_value / initial_value) ** (1 / years) - 1) * 100

def calculate_calmar_ratio(equity_curve: Union[List[float], pd.Series], years: float) -> float:
    """
    Calculate the Calmar ratio (CAGR / Max Drawdown).
    
    Args:
        equity_curve: List or Series of equity values
        years: Number of years in the backtest period
    
    Returns:
        float: Calmar ratio
    """
    cagr = calculate_cagr(equity_curve, years)
    max_dd = calculate_max_drawdown(equity_curve)
    
    if max_dd == 0:
        return 0.0
    
    return cagr / max_dd

def calculate_sortino_ratio(returns: Union[List[float], pd.Series], risk_free_rate: float = 0.02) -> float:
    """
    Calculate the Sortino ratio of the strategy.
    
    Args:
        returns: List or Series of returns
        risk_free_rate: Annual risk-free rate (default: 2%)
    
    Returns:
        float: Sortino ratio
    """
    if isinstance(returns, list):
        returns = pd.Series(returns)
    
    # Convert returns to annual
    annual_returns = returns.mean() * 252
    
    # Calculate downside deviation
    downside_returns = returns[returns < 0]
    downside_deviation = downside_returns.std() * np.sqrt(252)
    
    if downside_deviation == 0:
        return 0.0
    
    return (annual_returns - risk_free_rate) / downside_deviation

def calculate_win_rate(trades: pd.DataFrame) -> float:
    """
    Calculate the win rate from a trade log.
    
    Args:
        trades: DataFrame containing trade information
    
    Returns:
        float: Win rate as a percentage
    """
    if trades.empty:
        return 0.0
    
    winning_trades = len(trades[trades['PnL'] > 0])
    total_trades = len(trades)
    
    return (winning_trades / total_trades) * 100

def calculate_profit_factor(trades: pd.DataFrame) -> float:
    """
    Calculate the profit factor (gross profit / gross loss).
    
    Args:
        trades: DataFrame containing trade information
    
    Returns:
        float: Profit factor
    """
    if trades.empty:
        return 0.0
    
    gross_profit = trades[trades['PnL'] > 0]['PnL'].sum()
    gross_loss = abs(trades[trades['PnL'] < 0]['PnL'].sum())
    
    if gross_loss == 0:
        return float('inf')
    
    return gross_profit / gross_loss

def calculate_average_trade(trades: pd.DataFrame) -> float:
    """
    Calculate the average trade PnL.
    
    Args:
        trades: DataFrame containing trade information
    
    Returns:
        float: Average trade PnL
    """
    if trades.empty:
        return 0.0
    
    return trades['PnL'].mean()

def calculate_recovery_factor(equity_curve: Union[List[float], pd.Series]) -> float:
    """
    Calculate the recovery factor (total return / max drawdown).
    
    Args:
        equity_curve: List or Series of equity values
    
    Returns:
        float: Recovery factor
    """
    total_return = calculate_total_return(equity_curve)
    max_dd = calculate_max_drawdown(equity_curve)
    
    if max_dd == 0:
        return 0.0
    
    return total_return / max_dd 