"""
SSI Data Loader Module
Main interface for loading ticker data with caching and error handling
"""

import streamlit as st
from datetime import datetime
from .fetch import fetch_historical_price, validate_ticker
from .chart import create_ohlcv_candlestick, create_simple_line_chart


@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_ticker_price(ticker: str, start_date: str = None) -> 'plotly.graph_objects.Figure':
    """
    Load OHLCV data for a specific ticker and create chart.
    This is the main function used in the dashboard.
    
    Args:
        ticker (str): Stock ticker symbol
        start_date (str): Start date in 'YYYY-MM-DD' format
        
    Returns:
        plotly.graph_objects.Figure: Chart figure object
    """
    
    # Validate ticker
    if not validate_ticker(ticker):
        st.error(f"Invalid ticker symbol: {ticker}")
        return create_simple_line_chart(None, ticker, start_date)
    
    # Set default start date if not provided
    if start_date is None:
        start_date = datetime(datetime.today().year, 1, 1).strftime('%Y-%m-%d')
    
    # Fetch data
    df = fetch_historical_price(ticker, start_date)
    
    if df is None or df.empty:
        st.error(f"Unable to fetch data for ticker: {ticker}")
        return create_simple_line_chart(None, ticker, start_date)
    
    # Create chart
    try:
        fig = create_ohlcv_candlestick(df, ticker, start_date)
        
        # Debug: kiểm tra layout config trước khi return
        print(f"Debug - Chart created for {ticker}:")
        print(f"xaxis showgrid: {fig.layout.xaxis.showgrid}")
        print(f"xaxis tickformat: {fig.layout.xaxis.tickformat}")
        print(f"xaxis2 showgrid: {fig.layout.xaxis2.showgrid}")
        print(f"xaxis2 tickformat: {fig.layout.xaxis2.tickformat}")
        
        return fig
    except Exception as e:
        st.error(f"Error creating chart for {ticker}: {str(e)}")
        return create_simple_line_chart(df, ticker, start_date)


@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_ticker_data(ticker: str, start_date: str = None) -> 'pd.DataFrame':
    """
    Get raw ticker data without creating chart.
    Useful for data analysis or custom chart creation.
    
    Args:
        ticker (str): Stock ticker symbol
        start_date (str): Start date in 'YYYY-MM-DD' format
        
    Returns:
        pd.DataFrame: Raw OHLCV data
    """
    
    # Validate ticker
    if not validate_ticker(ticker):
        st.error(f"Invalid ticker symbol: {ticker}")
        return None
    
    # Set default start date if not provided
    if start_date is None:
        start_date = datetime(datetime.today().year, 1, 1).strftime('%Y-%m-%d')
    
    # Fetch data
    df = fetch_historical_price(ticker, start_date)
    
    if df is None or df.empty:
        st.error(f"Unable to fetch data for ticker: {ticker}")
        return None
    
    return df


def get_available_tickers() -> list:
    """
    Get a list of commonly used Vietnamese stock tickers.
    This is a static list for demonstration purposes.
    
    Returns:
        list: List of ticker symbols
    """
    return [
        'VNINDEX', 'VN30', 'HNX', 'HNX30',
        'TCB', 'VCB', 'BID', 'CTG', 'MBB', 'STB',
        'FPT', 'VNM', 'VIC', 'VHM', 'HPG', 'MSN',
        'SAB', 'BVH', 'GAS', 'PLX', 'POW', 'SHB'
    ]


def format_ticker_for_display(ticker: str) -> str:
    """
    Format ticker for better display in UI
    
    Args:
        ticker (str): Raw ticker symbol
        
    Returns:
        str: Formatted ticker symbol
    """
    if not ticker:
        return ""
    
    # Remove whitespace and convert to uppercase
    ticker = ticker.strip().upper()
    
    return ticker


def get_default_start_date() -> str:
    """
    Get default start date (beginning of current year)
    
    Returns:
        str: Default start date in 'YYYY-MM-DD' format
    """
    return datetime(datetime.today().year, 1, 1).strftime('%Y-%m-%d') 