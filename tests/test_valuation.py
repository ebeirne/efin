import sys
import os
import pytest

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import efin

def test_dividend_discount_model_valid():
    # Using a known ticker with dividends, e.g., KO (Coca-Cola)
    # User supplies a growth_rate of 3% and discount_rate (WACC) of 10%
    price = efin.dividend_discount_model("KO", growth_rate=0.03, discount_rate=0.1)
    assert isinstance(price, float)
    assert price > 0

def test_dividend_discount_model_no_dividends():
    # For a ticker that does not pay dividends (for example, TSLA might not pay dividends),
    # we expect a ValueError.
    with pytest.raises(ValueError):
        efin.dividend_discount_model("TSLA", growth_rate=0.03, discount_rate=0.1)

def test_comparable_company_analysis():
    # Test comparable analysis with target AAPL and peers MSFT and GOOGL.
    result = efin.comparable_company_analysis("AAPL", ["MSFT", "GOOGL"], multiple="trailingPE")
    expected_keys = {"target_ticker", "target_multiple", "avg_peer_multiple", "interpretation"}
    assert set(result.keys()) == expected_keys
    # Check that the returned multiples are positive numbers.
    assert result["target_multiple"] > 0
    assert result["avg_peer_multiple"] > 0

def test_residual_income_model_valid():
    # Using a known ticker (AAPL) and user-supplied values:
    # cost_of_equity of 10%, growth_rate of 5%, forecast period of 5 years.
    value = efin.residual_income_model("AAPL", cost_of_equity=0.1, growth_rate=0.05, forecast_period=5)
    assert isinstance(value, float)
    assert value > 0
