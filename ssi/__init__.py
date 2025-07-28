"""
SSI API Package
A comprehensive package for fetching and visualizing Vietnamese stock market data
"""

from .chart import create_ohlcv_candlestick, create_simple_line_chart

__version__ = "1.0.0"
__author__ = "Company Dashboard Team"

# Main functions to expose
__all__ = [
    'create_ohlcv_candlestick',
    'create_simple_line_chart'
]

# Try to import fetch functions if requests is available
try:
    from .fetch import fetch_historical_price, validate_ticker
    __all__.extend(['fetch_historical_price', 'validate_ticker'])
except ImportError:
    # Requests not available, fetch functions won't be exposed
    pass

# Try to import loader functions if streamlit is available
try:
    from .loader import load_ticker_price, get_ticker_data, get_available_tickers
    __all__.extend(['load_ticker_price', 'get_ticker_data', 'get_available_tickers'])
except ImportError:
    # Streamlit not available, loader functions won't be exposed
    pass 