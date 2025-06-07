import streamlit as st
from utils.data import fetch_data
import importlib
from utils.backtester import run_backtest
from utils import metrics
import plotly.graph_objects as go
import pandas as pd


st.set_page_config(page_title="Trading Bot Simulator", layout="wide")

st.title("🤖 Trading Bot Simulator")

# Sidebar Inputs
st.sidebar.header("🔧 Simulation Controls")
tickers = ["AAPL", "GOOG", "MSFT", "TSLA", "AMZN", "NVDA", "META"]
selected_ticker = st.sidebar.selectbox("Select Stock Ticker", tickers)

start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.date_input("End Date")

st.sidebar.markdown("---")

strategies = ["SMA Crossover", "RSI Strategy", "MACD Strategy"]
strategy_map = {
    "SMA Crossover": "sma_crossover",
    "RSI Strategy": "rsi_strategy",
    "MACD Strategy": "macd_strategy"
}
selected_strategy = st.sidebar.selectbox("Select Strategy", strategies)

run_button = st.sidebar.button("🚀 Run Simulation")

if run_button:
    st.subheader(f"📊 Results for {selected_ticker} from {start_date} to {end_date}")
    df = fetch_data(selected_ticker, start_date, end_date)
    close_prices = df["Close"].squeeze().tolist()

    # Strategy signals
    strategy_module_name = strategy_map[selected_strategy]
    strategy_module = importlib.import_module(f"strategies.{strategy_module_name}")
    signals = strategy_module.generate_signals(df)

    # Backtest
    equity_curve = run_backtest(df, signals)
    returns = equity_curve["Equity Curve"].pct_change().dropna().tolist()

    # Metrics
    total_ret = metrics.calculate_total_return(equity_curve["Equity Curve"].tolist())
    sharpe = metrics.calculate_sharpe_ratio(returns)
    max_dd = metrics.calculate_max_drawdown(equity_curve["Equity Curve"].tolist())

    # Layout: Tabs for visualization
    tab1, tab2, tab3 = st.tabs(["📈 Price & Trades", "📉 Equity Curve", "📊 Performance Metrics"])

    with tab1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df.index.tolist(),
            y=close_prices,
            mode='lines',
            name='Close Price',
            line=dict(color='blue')
        ))
        # Plot trades
        for i, signal in enumerate(signals):
            if signal == 'buy':
                fig.add_trace(go.Scatter(
                    x=[df.index[i]],
                    y=[close_prices[i]],
                    mode='markers',
                    marker=dict(color='green', size=10, symbol='triangle-up'),
                    name='Buy'
                ))
            elif signal == 'sell':
                fig.add_trace(go.Scatter(
                    x=[df.index[i]],
                    y=[close_prices[i]],
                    mode='markers',
                    marker=dict(color='red', size=10, symbol='triangle-down'),
                    name='Sell'
                ))
        fig.update_layout(
            title=f"{selected_ticker} Price with Trades",
            xaxis_title='Date',
            yaxis_title='Price',
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.line_chart(equity_curve['Equity Curve'])

    with tab3:
        col1, col2, col3 = st.columns(3)
        col1.metric("📈 Total Return", f"{total_ret:.2f}%")
        col2.metric("📊 Sharpe Ratio", f"{sharpe:.2f}")
        col3.metric("📉 Max Drawdown", f"{max_dd:.2f}%")

else:
    st.info("🎛️ Set parameters in the sidebar and click **Run Simulation** to begin.")


