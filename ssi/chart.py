"""
SSI Chart Creation Module
Handles creating beautiful candlestick charts with technical indicators
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st


def calculate_moving_averages(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate 20-day and 50-day moving averages
    
    Args:
        df (pd.DataFrame): DataFrame with OHLCV data
        
    Returns:
        pd.DataFrame: DataFrame with added MA columns
    """
    df = df.copy()
    
    # Calculate moving averages
    df['MA20'] = df['close'].rolling(window=20, min_periods=1).mean()
    df['MA50'] = df['close'].rolling(window=50, min_periods=1).mean()
    
    return df


def create_ohlcv_candlestick(df: pd.DataFrame, symbol: str, start_date: str = '2024-01-01') -> go.Figure:
    """
    Create a beautiful candlestick chart with volume and moving averages
    
    Args:
        df (pd.DataFrame): DataFrame with OHLCV data
        symbol (str): Stock symbol for title
        start_date (str): Start date for filtering data
        
    Returns:
        go.Figure: Plotly figure object
    """
    
    if df is None or df.empty:
        st.error("No data available to create chart")
        return go.Figure()
    
    # Filter data by start date
    df_temp = df[df['tradingDate'] >= start_date].copy()
    
    if df_temp.empty:
        st.warning(f"No data available from {start_date}")
        return go.Figure()
    
    # Calculate moving averages
    df_temp = calculate_moving_averages(df_temp)
    
    # Format dates for display
    df_temp['tradingDate'] = df_temp['tradingDate'].dt.strftime('%Y-%m-%d')
    
    # Create subplot with price and volume
    fig = make_subplots(
        rows=2, cols=1, 
        shared_xaxes=True, 
        vertical_spacing=0.03,
        row_heights=[0.7, 0.3],
        subplot_titles=[f"{symbol} Price Chart", "Volume"]
    )

    # Candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=df_temp['tradingDate'],
            open=df_temp['open'],
            high=df_temp['high'],
            low=df_temp['low'],
            close=df_temp['close'],
            name='OHLC',
            opacity=0.8,
            increasing_line_color='#26A69A',
            decreasing_line_color='#EF5350'
        ), row=1, col=1
    )
    
    # Moving Average 20
    fig.add_trace(
        go.Scatter(
            x=df_temp['tradingDate'],
            y=df_temp['MA20'],
            mode='lines',
            name='MA(20)',
            line=dict(color='#FF9800', width=2),
            opacity=0.8
        ), row=1, col=1
    )
    
    # Moving Average 50
    fig.add_trace(
        go.Scatter(
            x=df_temp['tradingDate'],
            y=df_temp['MA50'],
            mode='lines',
            name='MA(50)',
            line=dict(color='#2196F3', width=2),
            opacity=0.8
        ), row=1, col=1
    )
    
    # Volume bars with color coding
    colors = ['#26A69A' if c >= o else '#EF5350' for c, o in zip(df_temp['close'], df_temp['open'])]
    fig.add_trace(
        go.Bar(
            x=df_temp['tradingDate'],
            y=df_temp['volume'],
            marker_color=colors,
            name='Volume',
            opacity=0.6
        ), row=2, col=1
    )
    
    # Update layout for better appearance
    fig.update_layout(
        template='plotly_white',
        title={
            'text': f"{symbol} Price Chart",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': '#2E3440'}
        },
        xaxis2_title="Date",
        yaxis_title="Price (VND)",
        yaxis2_title="Volume",
        xaxis_rangeslider_visible=False,  
        xaxis2_rangeslider_visible=False,
        height=700,
        width=1200,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='rgba(0,0,0,0.1)',
            borderwidth=1
        ),
        margin=dict(l=50, r=50, t=80, b=50),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    # Update axes
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(0,0,0,0.1)',
        type='category',
        tickangle=45
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(0,0,0,0.1)',
        zeroline=False
    )
    
    # Update y-axis for volume
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(0,0,0,0.1)',
        zeroline=False,
        row=2, col=1
    )

    return fig


def create_simple_line_chart(df: pd.DataFrame, symbol: str, start_date: str = '2024-01-01') -> go.Figure:
    """
    Create a simple line chart for cases where candlestick data is not available
    
    Args:
        df (pd.DataFrame): DataFrame with price data
        symbol (str): Stock symbol for title
        start_date (str): Start date for filtering data
        
    Returns:
        go.Figure: Plotly figure object
    """
    
    if df is None or df.empty:
        st.error("No data available to create chart")
        return go.Figure()
    
    # Filter data by start date
    df_temp = df[df['tradingDate'] >= start_date].copy()
    
    if df_temp.empty:
        st.warning(f"No data available from {start_date}")
        return go.Figure()
    
    # Format dates for display
    df_temp['tradingDate'] = df_temp['tradingDate'].dt.strftime('%Y-%m-%d')
    
    fig = go.Figure()
    
    # Add close price line
    fig.add_trace(
        go.Scatter(
            x=df_temp['tradingDate'],
            y=df_temp['close'],
            mode='lines',
            name='Close Price',
            line=dict(color='#2196F3', width=2)
        )
    )
    
    # Update layout
    fig.update_layout(
        title=f"{symbol} Price Chart",
        xaxis_title="Date",
        yaxis_title="Price (VND)",
        template='plotly_white',
        height=500,
        showlegend=True
    )
    
    return fig 