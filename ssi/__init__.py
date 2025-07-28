"""
SSI API Package
A comprehensive package for fetching and visualizing Vietnamese stock market data
"""

from .loader import load_ticker_price, get_ticker_data, get_available_tickers
from .fetch import fetch_historical_price, validate_ticker
from .chart import create_ohlcv_candlestick, create_simple_line_chart

__version__ = "1.0.0"
__author__ = "Company Dashboard Team"

# Main functions to expose
__all__ = [
    'load_ticker_price',
    'get_ticker_data', 
    'get_available_tickers',
    'fetch_historical_price',
    'validate_ticker',
    'create_ohlcv_candlestick',
    'create_simple_line_chart'
] 