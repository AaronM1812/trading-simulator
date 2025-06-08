#importing pandas, used in the backtest function
import pandas as pd

#backtest function which takes in the dataframe, the signals, and the initial capital and performs the strategy on a portfolio
def run_backtest(df, signals, initial_capital=10000):
    #setting the data
    df = df.copy()
    df["Signal"] = signals
    prices = df["Close"]

    if isinstance(prices, pd.DataFrame):
        prices = prices.squeeze()
    prices = prices.tolist()

    signal_list = signals if isinstance(signals, list) else signals.tolist()

    #intial shared and cash
    shares = 0
    cash = initial_capital
    
    #creating lists for shares, cash, holdings and total value of portfolio
    shares_list = []
    cash_list = []
    holdings_list = []
    total_value_list = []
    
    #iterating though the prices and signals in the tuple and buying or selling
    for price, signal in zip(prices, signal_list):
        #passing if invalid
        if pd.isna(signal):
            pass
        #buying if the signal is buy and there is cash available
        elif signal == "buy" and cash > 0:
            #buying as many shares as possible and reducing the cash correspondingly
            shares = int(cash // price)
            cash -= shares * price
        #selling if the signal is sell and there are shares to sell in the portfolio
        elif signal == "sell" and shares > 0:
            #increasing the cash buy the value of the shares and restting the shares to 0
            cash += shares * price
            shares = 0
        
        #getting the current holdings and total value which is the holding value of shares plus the cash
        holdings = shares * price
        total_value = cash + holdings
        
        #adding these values to the shares, cash, holdings and total value lists
        shares_list.append(shares)
        cash_list.append(cash)
        holdings_list.append(holdings)
        total_value_list.append(total_value)
    
    #adding these to the dataframe as columns
    df["Shares"] = shares_list
    df["Cash"] = cash_list
    df["Holdings"] = holdings_list
    df["Total Value"] = total_value_list
    df["Equity Curve"] = df["Total Value"]
    
    #returning the dataframe
    return df
