import itertools
import numpy as np
import pandas as pd
import yfinance as yf
from statsmodels.tsa.arima.model import ARIMA
import logging

logger = logging.getLogger(__name__)

def auto_arima_grid_forecast(ticker, forecast_period=30, start_date='2010-01-01',
                             p_values=range(0, 3), d_values=range(0, 2), q_values=range(0, 3)):
    """
    Forecast stock prices using a manual grid search to select the best ARIMA model
    based on AIC.
    
    Parameters:
      ticker (str): Stock ticker (e.g., "AAPL").
      forecast_period (int): Number of days to forecast.
      start_date (str): Start date for historical data.
      p_values (iterable): Range of AR (p) parameters to try.
      d_values (iterable): Range of differencing (d) parameters to try.
      q_values (iterable): Range of MA (q) parameters to try.
      
    Returns:
      tuple: A tuple containing:
        - forecast_df (pandas.DataFrame): DataFrame with forecast dates and predicted prices.
        - best_order (tuple): The (p, d, q) order of the best model.
        - best_aic (float): The AIC value of the best model.
    """
    try:
        # Download historical data
        data = yf.download(ticker, start=start_date, auto_adjust=False)
        if "Adj Close" not in data.columns:
            raise ValueError("Adj Close column not found in data.")
        
        # Prepare DataFrame
        df = data[["Adj Close"]].reset_index()
        df.rename(columns={"Date": "ds", "Adj Close": "y"}, inplace=True)
        df["ds"] = pd.to_datetime(df["ds"])
        df.set_index("ds", inplace=True)
        
        best_aic = np.inf
        best_order = None
        best_model = None
        
        # Grid search over ARIMA parameters
        for order in itertools.product(p_values, d_values, q_values):
            try:
                model = ARIMA(df["y"], order=order).fit()
                if model.aic < best_aic:
                    best_aic = model.aic
                    best_order = order
                    best_model = model
            except Exception as e:
                logger.debug(f"ARIMA order {order} failed: {e}")
                continue
        
        if best_model is None:
            raise Exception("No valid ARIMA model found.")
        
        # Forecast future periods
        forecast = best_model.forecast(steps=forecast_period)
        last_date = df.index.max()
        forecast_dates = [last_date + pd.Timedelta(days=i) for i in range(1, forecast_period + 1)]
        
        forecast_df = pd.DataFrame({
            "ds": forecast_dates,
            "yhat": forecast
        })
        
        return forecast_df, best_order, best_aic
    except Exception as e:
        logger.error(f"Grid search ARIMA forecast error for {ticker}: {e}")
        raise
