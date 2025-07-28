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
    
    # Ensure datetime type for time axis - ép kiểu rõ ràng
    df_temp['tradingDate'] = pd.to_datetime(df_temp['tradingDate'], errors='coerce')
    # Remove any invalid dates
    df_temp = df_temp.dropna(subset=['tradingDate'])
    
    # Create subplot with price and volume
    fig = make_subplots(
        rows=2, cols=1, 
        shared_xaxes=True, 
        vertical_spacing=0.03,
        row_heights=[0.7, 0.3],
        subplot_titles=[f"{symbol} Price Chart", "Volume"]
    )

    # Tạo hover text thủ công cho candlestick
    hover_text = [
        f"<b>{d.strftime('%Y-%m-%d')}</b><br>"
        f"Open: {o:,.0f}<br>High: {h:,.0f}<br>Low: {l:,.0f}<br>Close: {c:,.0f}"
        for d, o, h, l, c in zip(df_temp['tradingDate'], df_temp['open'], df_temp['high'], df_temp['low'], df_temp['close'])
    ]

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
            decreasing_line_color='#EF5350',
            hoverinfo='text',
            hovertext=hover_text
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
            opacity=0.8,
            hovertemplate='<b>%{x|%Y-%m-%d}</b><br>' +
                         'MA(20): %{y:,.0f}<extra></extra>'
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
            opacity=0.8,
            hovertemplate='<b>%{x|%Y-%m-%d}</b><br>' +
                         'MA(50): %{y:,.0f}<extra></extra>'
        ), row=1, col=1
    )
    
    # Volume bars with color coding (convert to millions)
    colors = ['#26A69A' if c >= o else '#EF5350' for c, o in zip(df_temp['close'], df_temp['open'])]
    volume_m = df_temp['volume'] / 1_000_000  # Convert to millions
    fig.add_trace(
        go.Bar(
            x=df_temp['tradingDate'],
            y=volume_m,
            marker_color=colors,
            name='Volume',
            opacity=0.6,
            hovertemplate='<b>%{x|%Y-%m-%d}</b><br>' +
                         'Volume: %{y:.2f}M<extra></extra>'
        ), row=2, col=1
    )
    
    # Update layout for better appearance
    fig.update_layout(
        template='plotly_white',
        title=dict(
            text=f"{symbol} Price Chart",
            x=0.5,
            xanchor='center',
            font=dict(size=20, color='#2E3440')
        ),
        xaxis_rangeslider_visible=False,
        autosize=True,
        height=600,
        showlegend=True,
        hovermode='x unified',
        legend=dict(
            orientation="h",
            x=1,
            y=1.05,  # Tăng y để đè lên biểu đồ
            xanchor="center",  # Căn giữa
            yanchor="top",
            bgcolor='rgba(255,255,255,0)',
            borderwidth=0
        ),
        margin=dict(l=50, r=50, t=80, b=50),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    # X-Axis for both rows (hide vertical grid, show date format) - cách mạnh hơn
    fig.update_xaxes(
        showgrid=False,
        type='date',
        tickformat='%b %Y',
        tickangle=0,
        tickfont=dict(size=10)
    )

    # Y-Axis Price
    fig.update_yaxes(
        row=1, col=1,
        showgrid=True,
        gridcolor='rgba(0,0,0,0.01)',  # Nhẹ hơn
        zeroline=False,
        tickformat=',.0f'
    )

    # Y-Axis Volume
    fig.update_yaxes(
        row=2, col=1,
        showgrid=True,
        gridcolor='rgba(0,0,0,0.01)',  # Nhẹ hơn cho volume
        zeroline=False,
        tickformat='.2f',
        ticksuffix='M'
    )

    # Chỉ cập nhật hoverinfo cho Scatter và Bar (Volume), không cho Candlestick
    for trace in fig.data:
        if isinstance(trace, (go.Scatter, go.Bar)):
            trace.update(hoverinfo='x+y')
    
    # Force hide all vertical grids - cách mạnh hơn
    for axis in fig.layout:
        if axis.startswith("xaxis"):
            fig.layout[axis].update(showgrid=False)
    
    # Giải pháp mạnh cuối cùng: dùng fig.layout.update(...)
    fig.layout.update({
        'xaxis': dict(
            showgrid=False,
            tickformat='%b %Y',
            tickangle=0,
            tickfont=dict(size=10)
        ),
        'xaxis2': dict(
            showgrid=False,
            tickformat='%b %Y',
            tickangle=0,
            tickfont=dict(size=10)
        )
    })
    
    # Debug: kiểm tra layout config
    print("Final layout config:")
    print(fig.layout.to_plotly_json())

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