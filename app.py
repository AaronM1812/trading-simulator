import streamlit as st
from utils.data import fetch_data
import importlib
from utils.backtester import run_backtest

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

    strategy_module_name = strategy_map[selected_strategy]
    strategy_module = importlib.import_module(f"strategies.{strategy_module_name}")

    signals = strategy_module.generate_signals(df)

    equity_curve = run_backtest(df, signals)
    st.line_chart(equity_curve['Equity Curve'])
else:
    st.write("Set parameters and click 'Run Simulation' to start")
