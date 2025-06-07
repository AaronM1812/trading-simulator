import streamlit as st
from utils.data import fetch_data
import importlib
from utils.backtester import run_backtest
from utils import metrics
import plotly.graph_objects as go
import pandas as pd


st.title("Trading Bot Simulator")

st.sidebar.header("Simulation Controls")

tickers = ["AAPL", "GOOG", "MSFT", "TSLA", "AMZN", "NVDA", "META"]
selected_ticker = st.sidebar.selectbox("Select a stock ticker", tickers)

start_date = st.sidebar.date_input("Start date")
end_date = st.sidebar.date_input("End date")

strategies = ["SMA Crossover", "RSI Strategy", "MACD Strategy"]
strategy_map = {
    "SMA Crossover": "sma_crossover",
    "RSI Strategy": "rsi_strategy",
    "MACD Strategy": "macd_strategy"
}
selected_strategy = st.sidebar.selectbox("Select strategy", strategies)

if st.sidebar.button("Run Simulation"):
    st.write(f"Running simulation for {selected_ticker} from {start_date} to {end_date} using {selected_strategy}")

    df = fetch_data(selected_ticker, start_date, end_date)

    close_prices = df["Close"].squeeze().tolist()

    strategy_module_name = strategy_map[selected_strategy]
    strategy_module = importlib.import_module(f"strategies.{strategy_module_name}")
    signals = strategy_module.generate_signals(df)

    signal_list = signals.tolist()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index.tolist(),
        y=close_prices,
        mode='lines',
        name='Close Price',
        line=dict(color='blue')
    ))

    buy_indices = [i for i, s in enumerate(signal_list) if s == "buy"]
    sell_indices = [i for i, s in enumerate(signal_list) if s == "sell"]

    fig.add_trace(go.Scatter(
        x=[df.index[i] for i in buy_indices],
        y=[close_prices[i] for i in buy_indices],
        mode='markers',
        marker=dict(symbol='triangle-up', color='green', size=12),
        name='Buy Signals'
    ))

    fig.add_trace(go.Scatter(
        x=[df.index[i] for i in sell_indices],
        y=[close_prices[i] for i in sell_indices],
        mode='markers',
        marker=dict(symbol='triangle-down', color='red', size=12),
        name='Sell Signals'
    ))

    fig.update_layout(
        title=f"{selected_ticker} Price Chart",
        xaxis_title='Date',
        yaxis_title='Price',
        height=600
    )
    st.plotly_chart(fig, use_container_width=True)

    equity_curve = run_backtest(df, signals)
    returns = equity_curve["Equity Curve"].pct_change().dropna().tolist()

    total_ret = metrics.calculate_total_return(equity_curve["Equity Curve"].tolist())
    sharpe = metrics.calculate_sharpe_ratio(returns)
    max_dd = metrics.calculate_max_drawdown(equity_curve["Equity Curve"].tolist())

    st.line_chart(equity_curve['Equity Curve'])
    st.subheader("Performance Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Return", f"{total_ret:.2f}%")
    col2.metric("Sharpe Ratio", f"{sharpe:.2f}")
    col3.metric("Max Drawdown", f"{max_dd:.2f}%")

else:
    st.write("Set parameters and click 'Run Simulation' to start")

