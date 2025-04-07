import sys
import os
import pandas as pd

# Ensure the project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import efin

def download_adj_close_single():
    # Test downloading for a single ticker (should return a Series)
    data = efin.download_adj_close(["AAPL"], start_date="2020-01-01")
    # For a single ticker, our function returns a Series.
    assert isinstance(data, pd.Series)
    # Check that the Series is not empty
    assert not data.empty

def download_adj_close_multiple():
    # Test downloading for multiple tickers (should return a DataFrame)
    tickers = ["AAPL", "MSFT"]
    data = efin.download_adj_close(tickers, start_date="2020-01-01")
    # For multiple tickers, our function should return a DataFrame.
    assert isinstance(data, pd.DataFrame)
    # Check that the DataFrame is not empty
    assert not data.empty
    # Check that each ticker appears in the DataFrame columns.
    for ticker in tickers:
        assert ticker in data.columns
