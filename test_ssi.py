"""
Test script for the new SSI package
"""

import streamlit as st
from datetime import datetime
from ssi import load_ticker_price, get_available_tickers

# Test the new package
st.title("SSI Package Test")

# Test ticker selection
tickers = get_available_tickers()
selected_ticker = st.selectbox("Select a ticker to test:", tickers, index=0)

# Test date selection
ytd = datetime(datetime.today().year, 1, 1)
start_date = st.date_input("Start Date", value=ytd)

# Test the main function
if st.button("Load Chart"):
    try:
        fig = load_ticker_price(selected_ticker, start_date=start_date.strftime('%Y-%m-%d'))
        st.plotly_chart(fig, use_container_width=True)
        st.success(f"Successfully loaded chart for {selected_ticker}")
    except Exception as e:
        st.error(f"Error loading chart: {str(e)}")

# Display package info
st.sidebar.header("Package Info")
st.sidebar.write("SSI Package v1.0.0")
st.sidebar.write("Available tickers:", len(tickers)) 