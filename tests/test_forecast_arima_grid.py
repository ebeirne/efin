import sys
import os
import pandas as pd

# Ensure the project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from efin import auto_arima_grid_forecast

def test_auto_arima_grid_forecast_output():
    # Forecast for 5 days using the grid search auto ARIMA function.
    forecast_df, best_order, best_aic = auto_arima_grid_forecast("AAPL", forecast_period=5, start_date="2010-01-01")
    
    # Check that the output is a DataFrame.
    assert isinstance(forecast_df, pd.DataFrame)
    
    # Verify that the DataFrame contains the required columns.
    expected_columns = {"ds", "yhat"}
    assert expected_columns.issubset(set(forecast_df.columns))
    
    # Ensure the number of forecasted periods equals the forecast_period argument.
    assert len(forecast_df) == 5
    
    # Check that best_order is a tuple of three integers.
    assert isinstance(best_order, tuple)
    assert len(best_order) == 3
    for param in best_order:
        assert isinstance(param, int)
    
    # Check that best_aic is a float.
    assert isinstance(best_aic, float)
