#libraries used to calculate the performance metrics
import numpy as np
import pandas as pd
from typing import List, Union

#function to calculate the total return of the strategy
def calculate_total_return(equity_curve: Union[List[float], pd.Series]) -> float:
    #error handling if the equity curve is a list
    if isinstance(equity_curve, list):
        equity_curve = pd.Series(equity_curve)
    #initial value of the equity curve
    initial_value = equity_curve.iloc[0]
    #final value of the equity curve
    final_value = equity_curve.iloc[-1]
    #calculating the total return
    return ((final_value - initial_value) / initial_value) * 100

#function to calculate the sharpe ratio of the strategy
def calculate_sharpe_ratio(returns: Union[List[float], pd.Series], risk_free_rate: float = 0.02) -> float:
    #error handling if the returns are a list
    if isinstance(returns, list):
        returns = pd.Series(returns)
    
    #calculating the annual returns
    annual_returns = returns.mean() * 252
    #calculating the annual volatility
    annual_volatility = returns.std() * np.sqrt(252)
    #error handling if the annual volatility is 0
    if annual_volatility == 0:
        return 0.0
    #calculating the sharpe ratio
    return (annual_returns - risk_free_rate) / annual_volatility

#function to calculate the maximum drawdown of the strategy
def calculate_max_drawdown(equity_curve: Union[List[float], pd.Series]) -> float:
    #error handling if the equity curve is a list
    if isinstance(equity_curve, list):
        equity_curve = pd.Series(equity_curve)
    #calculating the running maximum
    running_max = equity_curve.expanding().max()
    #calculating the drawdowns
    drawdowns = (equity_curve - running_max) / running_max * 100
    #returning the maximum drawdown
    return abs(drawdowns.min())

def calculate_cagr(equity_curve: Union[List[float], pd.Series], years: float) -> float:
    #error handling if the equity curve is a list
    if isinstance(equity_curve, list):
        equity_curve = pd.Series(equity_curve)
    #initial value of the equity curve
    initial_value = equity_curve.iloc[0]
    #final value of the equity curve
    final_value = equity_curve.iloc[-1]
    #calculating the cagr
    return ((final_value / initial_value) ** (1 / years) - 1) * 100

#function to calculate the calmar ratio of the strategy
def calculate_calmar_ratio(equity_curve: Union[List[float], pd.Series], years: float) -> float:
    #error handling if the equity curve is a list
    if isinstance(equity_curve, list):
        equity_curve = pd.Series(equity_curve)
    #calculating the cagr
    cagr = calculate_cagr(equity_curve, years)
    max_dd = calculate_max_drawdown(equity_curve)
    #error handling if the max drawdown is 0
    if max_dd == 0:
        return 0.0
    #calculating the calmar ratio
    return cagr / max_dd

#function to calculate the sortino ratio of the strategy
def calculate_sortino_ratio(returns: Union[List[float], pd.Series], risk_free_rate: float = 0.02) -> float:
    #error handling if the returns are a list
    if isinstance(returns, list):
        returns = pd.Series(returns)
    
    #calculating the annual returns
    annual_returns = returns.mean() * 252
    #calculating the downside deviation
    downside_returns = returns[returns < 0]
    downside_deviation = downside_returns.std() * np.sqrt(252)
    #error handling if the downside deviation is 0
    if downside_deviation == 0:
        return 0.0
    #calculating the sortino ratio
    return (annual_returns - risk_free_rate) / downside_deviation

#function to calculate the win rate of the strategy
def calculate_win_rate(trades: pd.DataFrame) -> float:

    #error handling if the trades are empty
    if trades.empty:
        return 0.0
    #calculating the winning trades
    winning_trades = len(trades[trades['PnL'] > 0])
    #calculating the total trades
    total_trades = len(trades)
    #calculating the win rate
    return (winning_trades / total_trades) * 100

#function to calculate the profit factor of the strategy
def calculate_profit_factor(trades: pd.DataFrame) -> float:
    #error handling if the trades are empty
    if trades.empty:
        return 0.0
    #calculating the gross profit
    gross_profit = trades[trades['PnL'] > 0]['PnL'].sum()
    #calculating the gross loss
    gross_loss = abs(trades[trades['PnL'] < 0]['PnL'].sum())
    #error handling if the gross loss is 0
    if gross_loss == 0:
        return float('inf')
    #calculating the profit factor
    return gross_profit / gross_loss

#function to calculate the average trade of the strategy
def calculate_average_trade(trades: pd.DataFrame) -> float:
    #error handling if the trades are empty
    if trades.empty:
        return 0.0
    #calculating the average trade
    return trades['PnL'].mean()

#function to calculate the recovery factor of the strategy
def calculate_recovery_factor(equity_curve: Union[List[float], pd.Series]) -> float:
    #calculating the total return
    total_return = calculate_total_return(equity_curve)
    #calculating the max drawdown
    max_dd = calculate_max_drawdown(equity_curve)
    #error handling if the max drawdown is 0
    if max_dd == 0:
        return 0.0
    #calculating the recovery factor
    return total_return / max_dd 