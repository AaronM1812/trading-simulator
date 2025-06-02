import pandas as pd

#the function that implements the strategy on an initial portfolio and returns the data frame with a new column called portfolio which shows the value of the portfolio over time
def run_backtest(df, signals, initial_capital=10_000):
    #takes in the data frame and the signals from the strategy, note the data frame must have the close column for the closing prices, and also the intial cash, default 10k
    df = df.copy()
    #sets the dataframe columns to their associated values
    df["Signal"] = signals
    df["Shares"] = 0
    df["Cash"] = initial_capital
    df["Holdings"] = 0.0
    df["Total Value"] = initial_capital

    #the initial cash set to the capitals and number of shares to 0
    cash = initial_capital
    shares = 0

    #iterating through to get prices and signals
    for i in range(len(df)):
        price = df["Close"].iloc[i]
        signal = df["Signal"].iloc[i]

        #logic to buy or sell based on signal and current cash/position
        if signal == "buy" and cash > 0:
            shares = cash // price  # buy full shares only
            cash -= shares * price
        elif signal == "sell" and shares > 0:
            cash += shares * price
            shares = 0

        #the amount of holdings is the shares times the price
        holdings = shares * price
        #the total value of the portfolio is the cash held plus the holdings
        total = cash + holdings

        #adding the shares, cash, holdings and total portfolio value to the dataframe
        df.at[df.index[i], "Shares"] = shares
        df.at[df.index[i], "Cash"] = cash
        df.at[df.index[i], "Holdings"] = holdings
        df.at[df.index[i], "Total Value"] = total

    #the equity curve column set to the total value column
    df["Equity Curve"] = df["Total Value"]
    
    #returing the dataframe
    return df
