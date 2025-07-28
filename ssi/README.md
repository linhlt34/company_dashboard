# SSI Package

A comprehensive Python package for fetching and visualizing Vietnamese stock market data from TCBS API.

## Features

- **Enhanced Charts**: Beautiful candlestick charts with MA(20) and MA(50) indicators
- **Error Handling**: Comprehensive error handling and user-friendly warnings
- **Caching**: Built-in caching for improved performance
- **Modular Design**: Clean separation of concerns with dedicated modules

## Structure

```
ssi/
├── __init__.py      # Package initialization and exports
├── fetch.py         # API data fetching with error handling
├── chart.py         # Chart creation with technical indicators
├── loader.py        # Main interface for dashboard integration
└── README.md        # This documentation
```

## Usage

### Basic Usage

```python
from ssi import load_ticker_price

# Load chart for a ticker
fig = load_ticker_price('VNINDEX', start_date='2024-01-01')
```

### In Streamlit Dashboard

```python
import streamlit as st
from ssi import load_ticker_price
from datetime import datetime

# Get default start date (beginning of current year)
ytd = datetime(datetime.today().year, 1, 1)

# Create chart
fig = load_ticker_price(selected_ticker, start_date=ytd.strftime('%Y-%m-%d'))
st.plotly_chart(fig)
```

## Functions

### Main Functions

- `load_ticker_price(ticker, start_date)`: Main function for loading ticker data and creating charts
- `get_ticker_data(ticker, start_date)`: Get raw OHLCV data without chart creation
- `get_available_tickers()`: Get list of commonly used Vietnamese stock tickers

### Chart Functions

- `create_ohlcv_candlestick(df, symbol, start_date)`: Create candlestick chart with MA indicators
- `create_simple_line_chart(df, symbol, start_date)`: Create simple line chart as fallback

### Utility Functions

- `fetch_historical_price(ticker, start_date)`: Fetch data from TCBS API
- `validate_ticker(ticker)`: Validate ticker symbol format

## Chart Features

### Technical Indicators

- **MA(20)**: 20-day moving average (orange line)
- **MA(50)**: 50-day moving average (blue line)
- **Volume**: Color-coded volume bars (green for up, red for down)

### Visual Enhancements

- **Beautiful Layout**: Clean, professional appearance
- **Clear Legend**: Horizontal legend with proper positioning
- **Grid Lines**: Subtle grid lines for better readability
- **Color Coding**: Green/red candlesticks and volume bars
- **Responsive Design**: Optimized for different screen sizes

## Error Handling

The package includes comprehensive error handling:

- **Invalid Ticker**: Validates ticker format and shows appropriate errors
- **API Errors**: Handles network timeouts and API failures
- **Data Validation**: Checks for empty or invalid data
- **User-Friendly Messages**: Clear error messages for users

## Caching

Built-in caching for improved performance:

- **1-hour TTL**: Data is cached for 1 hour to reduce API calls
- **Automatic Refresh**: Cache automatically refreshes after expiration
- **Memory Efficient**: Uses Streamlit's caching system

## Example Tickers

Common Vietnamese stock tickers:

- **Indices**: VNINDEX, VN30, HNX, HNX30
- **Banks**: TCB, VCB, BID, CTG, MBB, STB
- **Large Caps**: FPT, VNM, VIC, VHM, HPG, MSN
- **Others**: SAB, BVH, GAS, PLX, POW, SHB

## Dependencies

- `requests`: For API calls
- `pandas`: For data manipulation
- `plotly`: For chart creation
- `streamlit`: For caching and UI integration

## Migration from SSI_API.py

The new package is fully backward compatible. Simply replace:

```python
# Old
from SSI_API import load_ticker_price

# New
from ssi import load_ticker_price
```

The function signature and behavior remain the same, but with enhanced features and better error handling. 