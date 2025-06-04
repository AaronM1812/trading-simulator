import pandas as pd

def run_backtest(df, signals, initial_capital=10000):
    df = df.copy()
    df["Signal"] = signals
    
    prices = df["Close"]
    if isinstance(prices, pd.DataFrame):
        prices = prices.squeeze()
    
    prices = prices.tolist()
    signal_list = signals.tolist()
    
    shares = 0
    cash = initial_capital
    
    shares_list = []
    cash_list = []
    holdings_list = []
    total_value_list = []
    
    for price, signal in zip(prices, signal_list):
        if pd.isna(signal):
            pass
        elif signal == "buy" and cash > 0:
            shares = int(cash // price)
            cash -= shares * price
        elif signal == "sell" and shares > 0:
            cash += shares * price
            shares = 0
        
        holdings = shares * price
        total_value = cash + holdings
        
        shares_list.append(shares)
        cash_list.append(cash)
        holdings_list.append(holdings)
        total_value_list.append(total_value)
    
    df["Shares"] = shares_list
    df["Cash"] = cash_list
    df["Holdings"] = holdings_list
    df["Total Value"] = total_value_list
    df["Equity Curve"] = df["Total Value"]
    
    return df
