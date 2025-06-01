import pandas as pd

#the function that implements the strategy on an initial portfolio and returns the data frame with a new column called portfolio which shows the value of the portfolio over time
def run_backtest(data, signal_col, initial_cash=10000):
    #takes in the data frame and the signals from the strategy, note the data frame must have the close column for the closing prices, and also the intial cash, default 10k

    cash = initial_cash
    # number of shares held
    position = 0
    #list to hold the portfolio value over time
    portfolio_values = []

    #iterating through the data to get the prices and the signals
    for date, row in data.iterrows():
        price = row['Close']
        signal = row[signal_col]

        #logic to buy or sell based on signal and current cash/position
        if signal == 'buy' and cash >= price:
            position = cash // price
            cash -= position * price
        elif signal == 'sell' and position > 0:
            cash += position * price
            position = 0

        #the total value of the portfolio is the cash held plus the value of the held shares
        total_value = cash + (position * price)
        #appending this portfolio value to the list
        portfolio_values.append(total_value)

    #adding the portfolio value column to the dataframe
    result = data.copy()
    result['Portfolio_Value'] = portfolio_values

    #and returning this dataframe
    return result
