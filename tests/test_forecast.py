import sys
import os
import pandas as pd

# Ensure the project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from efin import forecast

def test_forecast_output():
    # Use a known ticker with a forecast period of 5 days.
    forecast_df = forecast("AAPL", forecast_period=5, start_date="2010-01-01")
    
    # Check that the output is a DataFrame with the expected columns.
    assert isinstance(forecast_df, pd.DataFrame)
    expected_columns = {"ds", "yhat", "yhat_lower", "yhat_upper"}
    assert expected_columns.issubset(set(forecast_df.columns))
    
    # Check that the DataFrame has exactly 5 rows.
    assert len(forecast_df) == 5

    # Check that forecast dates are in ascending order.
    dates = pd.to_datetime(forecast_df["ds"])
    assert dates.is_monotonic_increasing
