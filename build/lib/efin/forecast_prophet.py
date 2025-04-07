import pandas as pd
import yfinance as yf
import numpy as np
from sklearn.linear_model import LinearRegression
import datetime
import logging

logger = logging.getLogger(__name__)

def forecast(ticker, forecast_period=30, start_date='2010-01-01'):
    """
    Forecast stock prices using a simple linear regression model.
    
    This function downloads historical adjusted close prices, converts dates
    to a numeric time variable (days since the first observation), fits a linear regression,
    and forecasts future prices for the specified number of days.
    
    Parameters:
      ticker (str): Stock ticker (e.g., "AAPL").
      forecast_period (int): Number of days to forecast.
      start_date (str): Start date for historical data.
    
    Returns:
      pandas.DataFrame: A DataFrame with columns:
          - ds: forecast dates
          - yhat: forecasted price
          - yhat_lower: lower bound (yhat - 1.96 * residual standard error)
          - yhat_upper: upper bound (yhat + 1.96 * residual standard error)
    """
    try:
        # Download historical data (non-adjusted so we can use "Adj Close")
        data = yf.download(ticker, start=start_date, auto_adjust=False)
        if "Adj Close" not in data.columns:
            raise ValueError("Adj Close column not found in data.")
        
        # Prepare the DataFrame
        df = data[["Adj Close"]].reset_index()
        df.rename(columns={"Date": "ds", "Adj Close": "y"}, inplace=True)
        df["ds"] = pd.to_datetime(df["ds"])
        
        # Create a numeric time variable: days since the first date
        df["t"] = (df["ds"] - df["ds"].min()).dt.days
        
        X = df[["t"]].values  # predictor: days
        y = df["y"].values      # response: price
        
        # Fit linear regression
        model = LinearRegression()
        model.fit(X, y)
        predictions = model.predict(X)
        residuals = y - predictions
        std_error = np.std(residuals)
        
        # Forecast future dates
        last_date = df["ds"].max()
        future_dates = [last_date + datetime.timedelta(days=i) for i in range(1, forecast_period + 1)]
        future_t = np.array([(d - df["ds"].min()).days for d in future_dates]).reshape(-1, 1)
        future_pred = model.predict(future_t).flatten()  # Ensure future_pred is 1D
        
        # Build the forecast DataFrame with 1D arrays for each column
        forecast_df = pd.DataFrame({
            "ds": future_dates,
            "yhat": future_pred,
            "yhat_lower": future_pred - 1.96 * std_error,
            "yhat_upper": future_pred + 1.96 * std_error
        })
        return forecast_df
    except Exception as e:
        logger.error(f"Forecast error for {ticker}: {e}")
        raise
