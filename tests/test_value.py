import sys
import os
import pytest

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import efin

def test_dcf_requires_rates():
    # Expect a ValueError if either rate is missing.
    with pytest.raises(ValueError):
        efin.dcf("AAPL", years=5, discount_rate=None, growth_rate=0.05)
    with pytest.raises(ValueError):
        efin.dcf("AAPL", years=5, discount_rate=0.10, growth_rate=None)

def test_dcf_with_valid_rates():
    # Using discount_rate=0.10 (10%) and growth_rate=0.05 (5%)
    # Since discount_rate > growth_rate, forecasted FCFs should increase, but discounted FCFs should decrease.
    result = efin.dcf("AAPL", years=5, discount_rate=0.10, growth_rate=0.05, terminal_growth_rate=0.02)
    expected_keys = {"forecast_fcfs", "discounted_fcfs", "terminal_value", "discounted_terminal_value", "total_dcf_value"}
    assert set(result.keys()) == expected_keys
    
    # Total DCF value should be positive.
    assert result["total_dcf_value"] > 0

    # Forecasted FCFs (before discounting) should be increasing.
    forecast_values = list(result["forecast_fcfs"].values())
    assert all(forecast_values[i] < forecast_values[i+1] for i in range(len(forecast_values) - 1))
    
    # Discounted FCFs should be decreasing (since discount rate > growth rate).
    discounted_values = list(result["discounted_fcfs"].values())
    assert all(discounted_values[i] > discounted_values[i+1] for i in range(len(discounted_values) - 1))