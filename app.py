import streamlit as st
from utils.data import fetch_data
import importlib
from utils.backtester import run_backtest
from utils import metrics


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
