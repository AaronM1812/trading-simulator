"""
Trading Bot Simulator - Main App
A Streamlit-based platform for backtesting trading strategies on historical stock data.
"""

import streamlit as st
from datetime import datetime, timedelta
import plotly.graph_objects as go
import pandas as pd

from app.data.market_data import fetch_market_data
from app.core.backtester import Backtester
from app.metrics.performance import (
    calculate_total_return,
    calculate_sharpe_ratio,
    calculate_max_drawdown,
    calculate_cagr,
    calculate_sortino_ratio,
    calculate_calmar_ratio,
)
from app.strategies.strategy_factory import get_strategy

# Set up the Streamlit page
st.set_page_config(
    page_title="Trading Bot Simulator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    # Only set up session state if it doesn't exist yet
    if 'last_run' not in st.session_state:
        st.session_state.last_run = None

def render_sidebar():
    st.sidebar.header("⚙️ Simulation Controls")
    
    # Ticker selection
    tickers = ["AAPL", "GOOG", "MSFT", "TSLA", "AMZN", "NVDA", "META"]
    selected_ticker = st.sidebar.selectbox("Select a stock ticker", tickers)
    
    # Date range selection (default: past year)
    today = datetime.now().date()
    default_start = today - timedelta(days=365)

    selected_start_date = st.sidebar.date_input(
        "Start date",
        value=default_start,
        max_value=today
    )
    selected_end_date = st.sidebar.date_input(
        "End date",
        value=today,
        max_value=today
    )
    # Prevent future dates and warn user if needed
    if selected_end_date > today:
        st.sidebar.warning("End date cannot be in the future. Resetting to today.")
        selected_end_date = today
    if selected_start_date > today:
        st.sidebar.warning("Start date cannot be in the future. Resetting to 1 year ago.")
        selected_start_date = default_start
    if selected_start_date >= selected_end_date:
        st.sidebar.error("Oops! Start date must be before end date. Please adjust your selection.")
        return None
    
    st.sidebar.markdown("---")
    st.sidebar.info("Tip: Hover over the parameter names for more info.")
    # TODO: Maybe add a logo or theme color later
    
    # Strategy selection
    strategies = ["SMA Crossover", "RSI Strategy", "MACD Strategy", "Bollinger Bands"]
    selected_strategy = st.sidebar.selectbox("Select strategy", strategies)
    
    # Get parameters for the selected strategy
    strategy_params = get_strategy_parameters(selected_strategy)
    
    # Run button
    run_button = st.sidebar.button("🚀 Run Simulation")
    
    return {
        'ticker': selected_ticker,
        'start_date': selected_start_date,
        'end_date': selected_end_date,
        'strategy': selected_strategy,
        'params': strategy_params,
        'run_button': run_button
    }

def get_strategy_parameters(strategy_name: str) -> dict:
    # Show parameter controls for the selected strategy
    params = {}
    if strategy_name == "SMA Crossover":
        params["short_window"] = st.sidebar.number_input(
            "Short Window", min_value=1, max_value=100, value=20,
            help="Number of days for the short moving average"
        )
        params["long_window"] = st.sidebar.number_input(
            "Long Window", min_value=1, max_value=200, value=50,
            help="Number of days for the long moving average"
        )
    elif strategy_name == "RSI Strategy":
        params["period"] = st.sidebar.number_input(
            "RSI Period", min_value=1, max_value=50, value=14,
            help="Number of days to calculate RSI"
        )
        params["overbought"] = st.sidebar.slider(
            "Overbought Threshold", 50, 100, 70,
            help="RSI value above which the asset is considered overbought"
        )
        params["oversold"] = st.sidebar.slider(
            "Oversold Threshold", 0, 50, 30,
            help="RSI value below which the asset is considered oversold"
        )
    elif strategy_name == "MACD Strategy":
        params["fast_period"] = st.sidebar.number_input(
            "Fast EMA Period", min_value=1, max_value=50, value=12,
            help="Number of days for the fast EMA in MACD"
        )
        params["slow_period"] = st.sidebar.number_input(
            "Slow EMA Period", min_value=1, max_value=100, value=26,
            help="Number of days for the slow EMA in MACD"
        )
        params["signal_period"] = st.sidebar.number_input(
            "Signal Line Period", min_value=1, max_value=50, value=9,
            help="Number of days for the MACD signal line"
        )
    elif strategy_name == "Bollinger Bands":
        params["window"] = st.sidebar.number_input(
            "Window (Period)", min_value=5, max_value=100, value=20,
            help="Number of days for the moving average window"
        )
        params["num_std"] = st.sidebar.slider(
            "Num Std Devs", 1, 4, 2,
            help="Number of standard deviations for the bands"
        )
    return params

def plot_price_and_trades(df: pd.DataFrame, signals: list, ticker: str):
    # Plot the price chart and overlay buy/sell signals
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index.tolist(),
        y=df["Close"].values,
        mode='lines',
        name='Close Price',
        line=dict(color='blue')
    ))
    # Add markers for buy/sell signals
    for i, signal in enumerate(signals):
        if signal == 'buy':
            fig.add_trace(go.Scatter(
                x=[df.index[i]],
                y=[df["Close"].iloc[i]],
                mode='markers',
                marker=dict(color='green', size=10, symbol='triangle-up'),
                name='Buy'
            ))
        elif signal == 'sell':
            fig.add_trace(go.Scatter(
                x=[df.index[i]],
                y=[df["Close"].iloc[i]],
                mode='markers',
                marker=dict(color='red', size=10, symbol='triangle-down'),
                name='Sell'
            ))
    fig.update_layout(
        title=f"{ticker} Price with Trades",
        xaxis_title='Date',
        yaxis_title='Price',
        height=600
    )
    return fig

def main():
    st.title("🤖 Trading Bot Simulator")
    initialize_session_state()
    params = render_sidebar()
    if params and params['run_button']:
        st.session_state.last_run = datetime.now()
        st.subheader(
            f"📊 Results for {params['ticker']} from {params['start_date']} "
            f"to {params['end_date']} using {params['strategy']}"
        )
        try:
            # Download the price data
            df = fetch_market_data(params['ticker'], params['start_date'], params['end_date'])
            # Flatten columns if multi-indexed (yfinance sometimes does this)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = [col[0] for col in df.columns]
            if df.empty:
                st.error("No data found for the selected ticker and date range. Please choose a different range.")
                return
            # Get the strategy and generate signals
            strategy = get_strategy(params['strategy'])
            signals = strategy.generate_signals(df, **params['params'])
            # Run the backtest
            backtester = Backtester(df, signals)
            equity_curve = backtester.run()
            returns = equity_curve["Equity Curve"].pct_change().dropna()
            # Calculate performance metrics
            total_ret = calculate_total_return(equity_curve["Equity Curve"])
            sharpe = calculate_sharpe_ratio(returns)
            max_dd = calculate_max_drawdown(equity_curve["Equity Curve"])
            # Show some more advanced stats for the curious/quants
            years = (params['end_date'] - params['start_date']).days / 365.25
            cagr = calculate_cagr(equity_curve["Equity Curve"], years)
            sortino = calculate_sortino_ratio(returns)
            calmar = calculate_calmar_ratio(equity_curve["Equity Curve"], years)
            # Tabs for results
            tab1, tab2, tab3 = st.tabs(["📈 Price & Trades", "📉 Equity Curve", "📊 Performance Metrics"])
            with tab1:
                fig = plot_price_and_trades(df, signals, params['ticker'])
                st.plotly_chart(fig, use_container_width=True)
            with tab2:
                st.line_chart(equity_curve['Equity Curve'])
            with tab3:
                col1, col2, col3 = st.columns(3)
                col1.metric("📈 Total Return", f"{total_ret:.2f}%")
                col2.metric("📊 Sharpe Ratio", f"{sharpe:.2f}")
                col3.metric("📉 Max Drawdown", f"{max_dd:.2f}%")
                st.markdown("#### Advanced Metrics")
                st.write(f"**CAGR:** {cagr:.2f}%")
                st.write(f"**Sortino Ratio:** {sortino:.2f}")
                st.write(f"**Calmar Ratio:** {calmar:.2f}")
                st.markdown("### Trade Log")
                trade_log = backtester.get_trade_log()
                if not trade_log.empty:
                    # Make sure all columns are scalars for Streamlit
                    for col in trade_log.columns:
                        trade_log[col] = trade_log[col].apply(lambda x: x if not hasattr(x, 'to_list') and not isinstance(x, (pd.Series, list, dict)) else str(x))
                st.dataframe(trade_log)
                st.download_button(
                    "📥 Download Trade Log",
                    trade_log.to_csv(index=False),
                    "trade_log.csv",
                    "text/csv"
                )
        except Exception as e:
            st.error(f"Something went wrong: {e}")
    else:
        st.info("🎛️ Set parameters in the sidebar and click **Run Simulation** to begin.")

if __name__ == "__main__":
    main()
# TODO: Add more strategies and risk management options in the next phase 