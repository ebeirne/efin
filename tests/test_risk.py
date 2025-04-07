import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from efin.risk import calculate_volatility, sharpe_ratio

def test_calculate_volatility():
    vol = calculate_volatility("AAPL", start_date="2020-01-01")
    assert vol > 0

def test_sharpe_ratio():
    sr = sharpe_ratio("AAPL", risk_free_rate=0.01, start_date="2020-01-01")
    # Sharpe ratio can be negative, but it must be a float.
    assert isinstance(sr, float)
