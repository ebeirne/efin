import sys
import os
import pandas as pd

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from efin import forecast

def test_forecast_output():
    # Use a known ticker with a forecast period of 5 days.
    forecast_df = forecast("AAPL", forecast_period=5, start_date="2015-01-01")
    
    # Check that the output is a DataFrame.
    assert isinstance(forecast_df, pd.DataFrame)
    
    # Verify that the DataFrame contains the required columns.
    expected_columns = {"ds", "yhat", "yhat_lower", "yhat_upper"}
    assert expected_columns.issubset(set(forecast_df.columns))
    
    # Ensure the number of forecasted periods equals the forecast_period argument.
    assert len(forecast_df) == 5

    # Optionally, you can check that the forecast dates are in ascending order.
    dates = pd.to_datetime(forecast_df["ds"])
    assert dates.is_monotonic_increasing
