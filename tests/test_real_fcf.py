import sys
import os
import pytest

# Ensure the project root is in sys.path so that efin can be imported.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from efin.value import _get_real_fcf

def test_get_real_fcf_returns_numeric():
    """
    Test that _get_real_fcf returns a numeric value (int or float)
    for a known ticker, and that it does not return the dummy value.
    """
    fcf = _get_real_fcf("AAPL")
    # Check that fcf is either an integer or a float
    assert isinstance(fcf, (int, float))
    # Check that the returned value is not equal to the dummy 80.0 value.
    # (Assuming that the real FCF is unlikely to exactly equal 80.0.)
    assert fcf != 80.0
