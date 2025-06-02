import pandas as pd

#this function will generate signals for the sma strategy, in which two smas are created, 10 and 20, when the 10 crosses above the 20, buy, and when it crosses below, sell, there is also logic to check the previous smas to prevent the same signals being generated, ensuring that the signal is only generated when the smas cross, else hold, i.e. the smas are equal
def generate_signals(data):
    """
    SMA crossover strategy:
    Buy when short MA crosses above long MA.
    Sell when short MA crosses below long MA.
    """
    #creating a dataframe copy and calculating both smas
    df = data.copy()
    df['SMA10'] = df['Close'].rolling(window=10).mean()
    df['SMA20'] = df['Close'].rolling(window=20).mean()

    df['Signal'] = None

    #generating the previous smas
    prev_sma10 = df['SMA10'].shift(1)
    prev_sma20 = df['SMA20'].shift(1)

    #logic to generate buy and sell signals
    buy_condition = (df['SMA10'] > df['SMA20']) & (prev_sma10 <= prev_sma20)
    sell_condition = (df['SMA10'] < df['SMA20']) & (prev_sma10 >= prev_sma20)

    #adding the signals buy and sell to the signal column, else if no signal is generated, hold
    df.loc[buy_condition, 'Signal'] = 'buy'
    df.loc[sell_condition, 'Signal'] = 'sell'
    df['Signal'].fillna('hold', inplace=True)

    return df
