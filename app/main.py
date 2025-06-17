#libraries used for the main fie, these are used to build the UI, handling dates, plotting charts and data manipulation
import streamlit as st
from datetime import datetime, timedelta
import plotly.graph_objects as go
import pandas as pd

#these are custom imports from my data, backtesting, metrics and strategies modules
from data.market_data import fetch_market_data
from core.backtester import Backtester
from metrics.performance import (
    calculate_total_return,
    calculate_sharpe_ratio,
    calculate_max_drawdown,
    calculate_cagr,
    calculate_sortino_ratio,
    calculate_calmar_ratio,
)
from strategies.strategy_factory import get_strategy

#setting up the steamlit page with title ext
st.set_page_config(
    page_title="Trading Bot Simulator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

#only creates the session state if it doesn't exist yet, prevents reruns and also used to show last updated timestamps
def initialize_session_state():
    if 'last_run' not in st.session_state:
        st.session_state.last_run = None

#the sidebar configuration which includes header, stock selection, date selection, strat selection and parameters and run button
def render_sidebar():
    st.sidebar.header("⚙️ Simulation Controls")
    
    #stock selection
    tickers = ["AAPL", "GOOG", "MSFT", "TSLA", "AMZN", "NVDA", "META"]
    selected_ticker = st.sidebar.selectbox("Select a stock ticker", tickers)
    
    #date selection
    today = datetime.now().date()
    #set start date to 1 year before
    default_start = today - timedelta(days=365)

    #this is the default start date
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
    
    #error handling of the user trying to select future dates and setting start infront of end
    if selected_end_date > today:
        st.sidebar.warning("End date cannot be in the future. Resetting to today.")
        selected_end_date = today
    if selected_start_date > today:
        st.sidebar.warning("Start date cannot be in the future. Resetting to 1 year ago.")
        selected_start_date = default_start
    if selected_start_date >= selected_end_date:
        st.sidebar.error("Oops! Start date must be before end date. Please adjust your selection.")
        return None
    
    #split the sidebare
    st.sidebar.markdown("---")
    #tip info
    st.sidebar.info("Tip: Hover over the parameter names for more info.")
    
    #strat selection
    strategies = ["SMA Crossover", "RSI Strategy", "MACD Strategy", "Bollinger Bands"]
    selected_strategy = st.sidebar.selectbox("Select strategy", strategies)
    
    #parameters of selected strat using get strategy parameters function below
    strategy_params = get_strategy_parameters(selected_strategy)
    
    #run button
    run_button = st.sidebar.button("🚀 Run Simulation")
    
    #all user inputs, used when passing parameters to simulation logic
    return {
        'ticker': selected_ticker,
        'start_date': selected_start_date,
        'end_date': selected_end_date,
        'strategy': selected_strategy,
        'params': strategy_params,
        'run_button': run_button
    }

#function for ui parameter controls based on selected strategy
def get_strategy_parameters(strategy_name: str) -> dict:
    #dictionary of parameter controls based on the strategy
    params = {}
    if strategy_name == "SMA Crossover":
        #e.g. create a short window for sma crossover with default values and help icon
        params["short_window"] = st.sidebar.number_input(
            "Short Window", min_value=1, max_value=100, value=20,
            help="Number of days for the short moving average"
        )
        #also a long window parameter with similar settings
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
    #returning the parameters dictionary
    return params

#function which plots the price chart with the buy and sell triangles to represent the trades
def plot_price_and_trades(df: pd.DataFrame, signals: list, ticker: str):
    #plotting the price chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index.tolist(),
        y=df["Close"].values,
        mode='lines',
        name='Close Price',
        #line colour used for dark mode visibility
        line=dict(color='#FFA500')
    ))
    
    #iterating through all the signals to plot the buy and sell triangles
    for i, signal in enumerate(signals):
        #if the signal is a buy, plot a green triangle using the date and price
        if signal == 'buy':
            fig.add_trace(go.Scatter(
                x=[df.index[i]],
                y=[df["Close"].iloc[i]],
                mode='markers',
                marker=dict(color='green', size=10, symbol='triangle-up'),
                name='Buy'
            ))
        #else if the signal is a sell, plot a red triangle using the date and price
        elif signal == 'sell':
            fig.add_trace(go.Scatter(
                x=[df.index[i]],
                y=[df["Close"].iloc[i]],
                mode='markers',
                marker=dict(color='red', size=10, symbol='triangle-down'),
                name='Sell'
            ))
    #updating the layout of the chart and returns ready for display in streamlit
    fig.update_layout(
        title=f"{ticker} Price with Trades",
        xaxis_title='Date',
        yaxis_title='Price',
        height=600
    )
    return fig

#main function which is run intially, sets up the page, sidebar and runs the simulation when run button is clicked
def main():
    #title of the page
    st.title("🤖 Trading Bot Simulator")
    #initializing the session state
    initialize_session_state()
    #rendering the sidebar
    params = render_sidebar()
    #if the run button is clicked, run the simulation
    if params and params['run_button']:
        #setting the last run timestamp
        st.session_state.last_run = datetime.now()
        #subheader of the page
        st.subheader(
            f"📊 Results for {params['ticker']} from {params['start_date']} "
            f"to {params['end_date']} using {params['strategy']}"
        )
        try:
            #download the datafram using the data module and required parameters
            df = fetch_market_data(params['ticker'], params['start_date'], params['end_date'])
            #flattening columns if multi indexed
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = [col[0] for col in df.columns]
            #error handling if no data is found
            if df.empty:
                st.error("No data found for the selected ticker and date range. Please choose a different range.")
                return
            #getting the strategy and generating signals
            strategy = get_strategy(params['strategy'])
            signals = strategy.generate_signals(df, **params['params'])
            #running the backtester
            backtester = Backtester(df, signals)
            #equity curve set to the total value of the portfolio
            equity_curve = backtester.run()
            #calculating the returns
            returns = equity_curve["Equity Curve"].pct_change().dropna()
            #calculating performance metrics using the metrics module
            total_ret = calculate_total_return(equity_curve["Equity Curve"])
            sharpe = calculate_sharpe_ratio(returns)
            max_dd = calculate_max_drawdown(equity_curve["Equity Curve"])
            #calculating the more advanced metrics suc as cagr, sortino and calmar using metrics module
            years = (params['end_date'] - params['start_date']).days / 365.25
            cagr = calculate_cagr(equity_curve["Equity Curve"], years)
            sortino = calculate_sortino_ratio(returns)
            calmar = calculate_calmar_ratio(equity_curve["Equity Curve"], years)
            #tabs used for better UI to show price chart, equity curve and performance metrics
            tab1, tab2, tab3 = st.tabs(["📈 Price & Trades", "📉 Equity Curve", "📊 Performance Metrics"])
            with tab1:
                #plotting the price chart with the buy and sell triangles
                fig = plot_price_and_trades(df, signals, params['ticker'])
                st.plotly_chart(fig, use_container_width=True)
            #plotting the equity curve
            with tab2:
                st.line_chart(equity_curve['Equity Curve'])
            #displaying the performance metrics and trade log
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
                #error handling
                if not trade_log.empty:
                    #making sure all columns are scalars for Streamlit
                    for col in trade_log.columns:
                        trade_log[col] = trade_log[col].apply(lambda x: x if not hasattr(x, 'to_list') and not isinstance(x, (pd.Series, list, dict)) else str(x))
                #displaying the trade log
                st.dataframe(trade_log)
                #download button, allowing the user to download the trade log as a csv
                st.download_button(
                    "📥 Download Trade Log",
                    trade_log.to_csv(index=False),
                    "trade_log.csv",
                    "text/csv"
                )
        #error handling if the simulation fails
        except Exception as e:
            st.error(f"Something went wrong: {e}")
    #error handling if the run button is not clicked
        st.info("🎛️ Set parameters in the sidebar and click **Run Simulation** to begin.")

#main function to run the app
if __name__ == "__main__":
    main()