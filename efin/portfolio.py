import yfinance as yf
import pandas as pd

def download_adj_close(tickers, start_date='2010-01-01'):
    data = yf.download(tickers, start=start_date, auto_adjust=False)
    if data.empty:
        raise ValueError("No data was downloaded.")
    if isinstance(data.columns, pd.MultiIndex):
        if "Adj Close" in data.columns.get_level_values(0):
            return data.xs("Adj Close", level=0, axis=1)
        elif "Close" in data.columns.get_level_values(0):
            return data.xs("Close", level=0, axis=1)
        else:
            raise ValueError("Neither 'Adj Close' nor 'Close' found in the data.")
    else:
        if "Adj Close" in data.columns:
            return data["Adj Close"]
        elif "Close" in data.columns:
            return data["Close"]
        else:
            raise ValueError("Neither 'Adj Close' nor 'Close' found in the data.")


def markowitz_portfolio(returns):
    """
    A simple placeholder for Markowitz portfolio optimization.
    Returns equal weights for all assets.
    
    Parameters:
      returns (pandas.DataFrame): Historical returns for each asset.
    
    Returns:
      numpy.ndarray: An array of weights that sum to 1.
    """
    import numpy as np
    n = returns.shape[1]
    return np.repeat(1/n, n)
