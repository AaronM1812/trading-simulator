#importing the necessary files to calculate the performance metrics
import pandas as pd
import numpy as np

#total return function which takes in the equity list and returns a float which is the total percentage of return using the strategy
def calculate_total_return(equity_curve_list: list) -> float:
    #validity check
    if not equity_curve_list or len(equity_curve_list) < 2:
        return 0.0
    
    #returning the last total value divided by the inital total miuus 1 and multiplying this by 100 to get this as a percent
    return ((equity_curve_list[-1] / equity_curve_list[0]) - 1) * 100

#function which calculates the sharpe ratio using the equity list and risk rate and returning a float, measures risk-adjusted returns
def calculate_sharpe_ratio(equity_curve_list: list, risk_free_rate=0.01) -> float:
    #validity check
    if len(equity_curve_list) < 2:
        return 0.0
    #converting to a series for logic reasons
    equity_curve = pd.Series(equity_curve_list)
    
    #replace 0 or near zero with NaN to avoid division by zero
    equity_curve = equity_curve.replace(0, np.nan).dropna()
    
    #calculating the daily percentage returns
    daily_returns = equity_curve.pct_change().dropna()

    #subtracting the daily risk free rate from each return to get the excess return
    excess_returns = daily_returns - (risk_free_rate / 252)

    #avoiding division by 0
    if excess_returns.std() == 0:
        return 0.0
    
    #anualising the sharpe ratio
    return np.sqrt(252) * excess_returns.mean() / excess_returns.std()


#function which calculates the drawdown using the equity curve list and returns a float, the worst drop from a peak to a trough
def calculate_max_drawdown(equity_curve_list: list) -> float:
    #validity check
    if not equity_curve_list:
        return 0.0
    #converting to a series for logic
    equity_curve = pd.Series(equity_curve_list)

    #highest portfolio value seen so far
    running_max = equity_curve.cummax()

    #computes the drawdown from this point
    drawdown = (equity_curve - running_max) / running_max

    #returns the most negative drawdown seen so far, worst loss from a peak
    return drawdown.min()
