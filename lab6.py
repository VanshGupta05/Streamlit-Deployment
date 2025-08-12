import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Smart Stock Tracker", layout="wide")
st.title("Smart Stock Tracker")

if "watchlist" not in st.session_state:
    st.session_state.watchlist = []

st.sidebar.header("Stock Search")
ticker = st.sidebar.text_input("Enter Stock Symbol (e.g., RELIANCE.NS, INFY.NS):", value="RELIANCE.NS")
period = st.sidebar.selectbox("Select Time Period", ["5d", "1mo", "3mo", "6mo", "1y"], index=1)

if st.sidebar.button("Track Stock"):
    st.session_state.selected_stock = ticker.upper()

if "selected_stock" in st.session_state:
    stock = yf.Ticker(st.session_state.selected_stock)
    try:
        hist = stock.history(period=period)

        st.subheader(f"Price Trend for {st.session_state.selected_stock}")
        st.line_chart(hist["Close"])

        info = stock.info
        st.write("Company Name:", info.get("longName", "N/A"))
        st.write("Sector:", info.get("sector", "N/A"))
        st.write("Market Cap:", info.get("marketCap", "N/A"))

        if st.button("Add to Watchlist"):
            if st.session_state.selected_stock not in st.session_state.watchlist:
                st.session_state.watchlist.append(st.session_state.selected_stock)
                st.success("Added to watchlist")
            else:
                st.warning("Already in watchlist")
    except:
        st.error("Invalid stock symbol or data unavailable")

st.sidebar.header("Your Watchlist")
if st.session_state.watchlist:
    for stock in st.session_state.watchlist:
        st.sidebar.markdown(f"- {stock}")
else:
    st.sidebar.info("Watchlist is empty")

st.markdown("---")
st.markdown("Built with Streamlit and Yahoo Finance")
