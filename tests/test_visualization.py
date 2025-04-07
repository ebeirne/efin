import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from efin.visualization import plot_forecast
import pandas as pd
import numpy as np

def test_plot_forecast():
    dates_history = pd.date_range("2020-01-01", periods=50)
    history = pd.Series(np.random.randn(50).cumsum(), index=dates_history)
    
    dates_forecast = pd.date_range("2020-02-20", periods=10)
    forecast = pd.Series(np.random.randn(10).cumsum(), index=dates_forecast)
    
    # Simply ensure that the function runs without throwing an exception.
    try:
        plot_forecast(history, forecast, title="Test Plot")
    except Exception as e:
        assert False, f"plot_forecast raised an exception: {e}"
