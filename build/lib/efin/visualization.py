import matplotlib.pyplot as plt
import pandas as pd

def plot_forecast(history, forecast, title="Forecast vs History"):
    """
    Plot historical data and forecasted values.
    Parameters:
      history (pandas.Series): Historical time series.
      forecast (pandas.Series or DataFrame): Forecasted data.
    """
    plt.figure(figsize=(10, 5))
    plt.plot(history.index, history.values, label="History")
    if isinstance(forecast, pd.Series):
        plt.plot(forecast.index, forecast.values, label="Forecast")
    elif isinstance(forecast, pd.DataFrame):
        plt.plot(forecast['ds'], forecast['yhat'], label="Forecast")
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.show()
