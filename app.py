import streamlit as st
from utils.data import fetch_data

#title
st.title("Trading Bot Simulator")

#sidebar header
st.sidebar.header("Simulation Controls")

#ticker selection
tickers = ["AAPL", "GOOG", "MSFT", "TSLA", "AMZN", "NVDA", "META"]
selected_ticker = st.sidebar.selectbox("Select a stock ticker", tickers)

#data range selection
start_date = st.sidebar.date_input("Start date")
end_date = st.sidebar.date_input("End date")

#strategy selection
strategies = ["SMA Crossover", "RSI Strategy", "MACD Strategy"]
selected_strategy = st.sidebar.selectbox("Select strategy", strategies)

#run simulation button
if st.sidebar.button("Run Simulation"):
    st.write(f"Running simulation for {selected_ticker} from {start_date} to {end_date} using {selected_strategy}")

     # Fetch data
    df = fetch_data(selected_ticker, str(start_date), str(end_date))

    # Show preview
    st.subheader("📊 Price Data Preview")
    st.dataframe(df.head())
else:
    st.write("Set parameters and click 'Run Simulation' to start")
