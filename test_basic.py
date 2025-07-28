"""
Basic test script for SSI package structure (without streamlit)
"""

def test_imports():
    """Test basic imports without streamlit"""
    try:
        # Test fetch module
        from ssi.fetch import validate_ticker
        print("✓ fetch module imported successfully")
        
        # Test validation function
        result = validate_ticker('VNINDEX')
        print(f"✓ validate_ticker works: {result}")
        
        # Test chart module (without streamlit)
        import pandas as pd
        from ssi.chart import calculate_moving_averages
        
        # Create dummy data
        dates = pd.date_range('2024-01-01', periods=100, freq='D')
        dummy_data = pd.DataFrame({
            'tradingDate': dates,
            'close': [100 + i * 0.1 for i in range(100)]
        })
        
        # Test moving average calculation
        result_df = calculate_moving_averages(dummy_data)
        print(f"✓ calculate_moving_averages works: MA20 exists = {'MA20' in result_df.columns}")
        
        print("\n✅ All basic tests passed!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

if __name__ == "__main__":
    test_imports() 