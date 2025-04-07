import sys
import os
from click.testing import CliRunner

# Ensure the project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from efin import cli

def test_cli_forecast_linear():
    runner = CliRunner()
    result = runner.invoke(cli, ["forecast", "AAPL", "--model", "linear", "--period", "5"])
    # The output should contain the forecast header; adjust the expected string if needed.
    assert "Forecast for AAPL" in result.output

def test_cli_forecast_grid():
    runner = CliRunner()
    result = runner.invoke(cli, ["forecast", "AAPL", "--model", "grid", "--period", "5"])
    # The output should mention grid search; adjust the expected string if needed.
    assert "Grid search ARIMA Forecast for AAPL" in result.output
