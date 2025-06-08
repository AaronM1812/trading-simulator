#these are the libraries being used for this trading simulator
import streamlit as st
from utils.data import fetch_data
import importlib
from utils.backtester import run_backtest
from utils import metrics
import plotly.graph_objects as go
import pandas as pd

#creating a streamlit page
st.set_page_config(page_title="Trading Bot Simulator", layout="wide")

#title of the page
st.title("🤖 Trading Bot Simulator")

#sidebar header
st.sidebar.header("⚙️ Simulation Controls")

#stock dropdown selection input
tickers = ["AAPL", "GOOG", "MSFT", "TSLA", "AMZN", "NVDA", "META"]
selected_ticker = st.sidebar.selectbox("Select a stock ticker", tickers)

#date selection input
start_date = st.sidebar.date_input("Start date")
end_date = st.sidebar.date_input("End date")

#sidebar split
st.sidebar.markdown("---")

#strategy selection
strategies = ["SMA Crossover", "RSI Strategy", "MACD Strategy"]

#dictionary to map stratgey selection to parameter
strategy_map = {
    "SMA Crossover": "sma_crossover",
    "RSI Strategy": "rsi_strategy",
    "MACD Strategy": "macd_strategy"
}
selected_strategy = st.sidebar.selectbox("Select strategy", strategies)

strategy_params = {}

#strategy parameters including SMA windows, RSI period and threshold, MACD period and signal line period
if selected_strategy == "SMA Crossover":
    strategy_params["short_window"] = st.sidebar.number_input("Short Window", min_value=1, max_value=100, value=20)
    strategy_params["long_window"] = st.sidebar.number_input("Long Window", min_value=1, max_value=200, value=50)

elif selected_strategy == "RSI Strategy":
    strategy_params["period"] = st.sidebar.number_input("RSI Period", min_value=1, max_value=50, value=14)
    strategy_params["overbought"] = st.sidebar.slider("Overbought Threshold", 50, 100, 70)
    strategy_params["oversold"] = st.sidebar.slider("Oversold Threshold", 0, 50, 30)

elif selected_strategy == "MACD Strategy":
    strategy_params["fast_period"] = st.sidebar.number_input("Fast EMA Period", min_value=1, max_value=50, value=12)
    strategy_params["slow_period"] = st.sidebar.number_input("Slow EMA Period", min_value=1, max_value=100, value=26)
    strategy_params["signal_period"] = st.sidebar.number_input("Signal Line Period", min_value=1, max_value=50, value=9)

#run simulation button
run_button = st.sidebar.button("🚀 Run Simulation")

#logic if the button is clicked
if run_button:
    #title in the page using inputs
    st.subheader(f"📊 Results for {selected_ticker} from {start_date} to {end_date} using {selected_strategy}")

    #function call from data.py to fetch the data and return the dataframe
    df = fetch_data(selected_ticker, start_date, end_date)

    #getting the closing prices(used for logic and parameter passing)
    close_prices = df["Close"].values.flatten().tolist()

    #importing the selected strategies generate signal function using tthe map, then generating the buy/sell signals using this function
    strategy_module_name = strategy_map[selected_strategy]
    strategy_module = importlib.import_module(f"strategies.{strategy_module_name}")
    signals = strategy_module.generate_signals(df, **strategy_params)

    #function call to run the backtest from backtester.py which will return the equity curve
    equity_curve = run_backtest(df, signals)
    returns = equity_curve["Equity Curve"].pct_change().dropna().tolist()

    #using the equity curve and the returns generated above to work out the metrics such as total return, sharpe and max drawdown from the corresponding functions in metrics.py
    total_ret = metrics.calculate_total_return(equity_curve["Equity Curve"].tolist())
    sharpe = metrics.calculate_sharpe_ratio(returns)
    max_dd = metrics.calculate_max_drawdown(equity_curve["Equity Curve"].tolist())

    #creating steamlit tabs for cleaner UI
    tab1, tab2, tab3 = st.tabs(["📈 Price & Trades", "📉 Equity Curve", "📊 Performance Metrics"])

    #placing the price and trades in tab1
    with tab1:
        #creating the price chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df.index.tolist(),
            y=close_prices,
            mode='lines',
            name='Close Price',
            line=dict(color='blue')
        ))
        #creating the buy traingle annotations
        for i, signal in enumerate(signals):
            if signal == 'buy':
                fig.add_trace(go.Scatter(
                    x=[df.index[i]],
                    y=[close_prices[i]],
                    mode='markers',
                    marker=dict(color='green', size=10, symbol='triangle-up'),
                    name='Buy'
                ))
            #and also creating the sell triangle annptations
            elif signal == 'sell':
                fig.add_trace(go.Scatter(
                    x=[df.index[i]],
                    y=[close_prices[i]],
                    mode='markers',
                    marker=dict(color='red', size=10, symbol='triangle-down'),
                    name='Sell'
                ))
        #setting the graph
        fig.update_layout(
            title=f"{selected_ticker} Price with Trades",
            xaxis_title='Date',
            yaxis_title='Price',
            height=600
        )
        #and plotting it
        st.plotly_chart(fig, use_container_width=True)

    #placing the equity curve in tab 2 using streamlit line chart
    with tab2:
        st.line_chart(equity_curve['Equity Curve'])

    #placing the performance metrics calculated earlier into tab 3
    with tab3:
        col1, col2, col3 = st.columns(3)
        col1.metric("📈 Total Return", f"{total_ret:.2f}%")
        col2.metric("📊 Sharpe Ratio", f"{sharpe:.2f}")
        col3.metric("📉 Max Drawdown", f"{max_dd:.2f}%")

else:
    #if the simulation failed, provide user intructions
    st.info("🎛️ Set parameters in the sidebar and click **Run Simulation** to begin.")

