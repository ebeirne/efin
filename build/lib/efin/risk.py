import yfinance as yf
import pandas as pd

def _extract_price_series(data):
    """
    Extracts the price series from a DataFrame downloaded via yfinance.
    For multi-ticker data, checks both levels of the MultiIndex.
    """
    if isinstance(data.columns, pd.MultiIndex):
        if "Adj Close" in data.columns.get_level_values(0):
            series = data.xs("Adj Close", level=0, axis=1)
        elif "Adj Close" in data.columns.get_level_values(1):
            series = data.xs("Adj Close", level=1, axis=1)
        elif "Close" in data.columns.get_level_values(0):
            series = data.xs("Close", level=0, axis=1)
        elif "Close" in data.columns.get_level_values(1):
            series = data.xs("Close", level=1, axis=1)
        else:
            raise ValueError("Neither 'Adj Close' nor 'Close' found in the data.")
    else:
        if "Adj Close" in data.columns:
            series = data["Adj Close"]
        elif "Close" in data.columns:
            series = data["Close"]
        else:
            raise ValueError("Neither 'Adj Close' nor 'Close' found in the data.")
    return series.squeeze()

def calculate_volatility(ticker, start_date='2010-01-01'):
    """
    Calculates the volatility (standard deviation of daily returns) for the given ticker.
    """
    data = yf.download(ticker, start=start_date, auto_adjust=False)
    price_series = _extract_price_series(data)
    returns = price_series.pct_change().dropna()
    std_val = returns.std()
    # If std_val is a Series, convert it to a scalar (assuming one column)
    if isinstance(std_val, pd.Series):
        std_val = std_val.iloc[0]
    return std_val

def sharpe_ratio(ticker, risk_free_rate=0.01, start_date='2010-01-01'):
    """
    Calculates the Sharpe ratio for the given ticker.
    Adjusts the risk-free rate to a daily rate (assuming 252 trading days).
    """
    data = yf.download(ticker, start=start_date, auto_adjust=False)
    price_series = _extract_price_series(data)
    returns = price_series.pct_change().dropna()
    excess_returns = returns - (risk_free_rate / 252)
    ratio = excess_returns.mean() / excess_returns.std()
    if isinstance(ratio, pd.Series):
        ratio = ratio.iloc[0]
    return ratio
