"""
SSI API Data Fetching Module
Handles fetching historical stock price data from TCBS API
"""

import requests
import pandas as pd
from datetime import datetime
import streamlit as st


def fetch_historical_price(ticker: str, start_date: str = None) -> pd.DataFrame:
    """
    Fetch stock historical price and volume data from TCBS API
    
    Args:
        ticker (str): Stock ticker symbol (e.g., 'VNINDEX', 'TCB')
        start_date (str): Start date in 'YYYY-MM-DD' format
        
    Returns:
        pd.DataFrame: DataFrame with OHLCV data or None if error
    """
    
    # TCBS API endpoint for historical data
    url = "https://apipubaws.tcbs.com.vn/stock-insight/v1/stock/bars-long-term"
    
    # Convert start_date string to timestamp if provided
    if start_date:
        try:
            start_timestamp = str(int(datetime.strptime(start_date, "%Y-%m-%d").timestamp()))
        except ValueError:
            st.error(f"Invalid date format: {start_date}. Please use YYYY-MM-DD format.")
            return None
    else:
        # Default to 1 year ago if no start_date provided
        start_timestamp = str(int((datetime.now() - pd.Timedelta(days=365)).timestamp()))
    
    # Parameters for stock data
    params = {
        "ticker": ticker,
        "type": "stock",
        "resolution": "D",  # Daily data
        "from": start_timestamp,
        "to": str(int(datetime.now().timestamp()))
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if 'data' in data and data['data']:
            # Convert to DataFrame for easier manipulation
            df = pd.DataFrame(data['data'])
            
            # Convert timestamp to datetime
            if 'tradingDate' in df.columns:
                # Check if tradingDate is already in ISO format
                if df['tradingDate'].dtype == 'object' and df['tradingDate'].str.contains('T').any():
                    df['tradingDate'] = pd.to_datetime(df['tradingDate'])
                else:
                    df['tradingDate'] = pd.to_datetime(df['tradingDate'], unit='ms')
            
            # Select relevant columns
            columns_to_keep = ['tradingDate', 'open', 'high', 'low', 'close', 'volume']
            df = df[[col for col in columns_to_keep if col in df.columns]]
            
            # Sort by date
            df = df.sort_values('tradingDate')
            
            return df
        else:
            st.warning(f"No data found for ticker: {ticker}")
            return None
            
    except requests.exceptions.Timeout:
        st.error(f"Request timeout for ticker: {ticker}. Please try again.")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data for {ticker}: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Unexpected error for {ticker}: {str(e)}")
        return None


def validate_ticker(ticker: str) -> bool:
    """
    Basic validation for ticker symbol
    
    Args:
        ticker (str): Ticker symbol to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not ticker or not isinstance(ticker, str):
        return False
    
    # Remove whitespace and convert to uppercase
    ticker = ticker.strip().upper()
    
    # Basic validation - ticker should be alphanumeric
    if not ticker.isalnum():
        return False
    
    return True 