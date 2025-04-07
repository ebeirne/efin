import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
from efin.portfolio import download_adj_close, markowitz_portfolio
import numpy as np

def test_download_adj_close():
    tickers = ["AAPL", "MSFT"]
    data = download_adj_close(tickers, start_date="2020-01-01")
    assert isinstance(data, pd.DataFrame)
    for ticker in tickers:
        assert ticker in data.columns

def test_markowitz_portfolio():
    # Create dummy returns for testing
    returns = pd.DataFrame({
        "AAPL": np.random.normal(0.01, 0.02, 100),
        "MSFT": np.random.normal(0.015, 0.025, 100)
    })
    weights = markowitz_portfolio(returns)
    # Check that weights sum to 1 and that there is one weight per ticker.
    assert abs(sum(weights) - 1.0) < 1e-6
    assert len(weights) == returns.shape[1]
