import yfinance as yf
import logging

logger = logging.getLogger(__name__)

def _get_real_fcf(ticker):
    """
    Retrieve the base free cash flow (FCF) for the given ticker using yfinance.

    This function attempts to use the "Free Cash Flow" row from the cash flow statement.
    If that row is not present, it calculates FCF as:
         FCF = Total Cash From Operating Activities + Capital Expenditures
    Note: Values are returned as provided by yfinance and may be in millions or billions.

    Parameters:
      ticker (str): Stock ticker symbol (e.g., "AAPL").

    Returns:
      float: The free cash flow for the most recent period.

    Raises:
      ValueError: If no cash flow data or the required keys are found.
    """
    ticker_obj = yf.Ticker(ticker)
    cf = ticker_obj.cashflow
    if cf is None or cf.empty:
        raise ValueError(f"No cash flow data found for ticker {ticker}.")
    
    # Use "Free Cash Flow" if available
    if "Free Cash Flow" in cf.index:
        fcf = cf.loc["Free Cash Flow"].iloc[0]
        return fcf
    # Otherwise, compute FCF as: Operating Cash Flow + Capital Expenditures
    if "Operating Cash Flow" in cf.index and "Capital Expenditure" in cf.index:
        op_cf = cf.loc["Operating Cash Flow"].iloc[0]
        capex = cf.loc["Capital Expenditure"].iloc[0]
        fcf = op_cf + capex
        return fcf
    raise ValueError("Required cash flow data not found for ticker.")

def dcf(ticker, years, discount_rate, growth_rate, terminal_growth_rate=0.02):
    """
    Calculate the Discounted Cash Flow (DCF) valuation for a given stock ticker,
    using user-supplied growth rate and discount rate (WACC).

    Parameters:
      ticker (str): Stock ticker symbol (e.g., "AAPL").
      years (int): Forecast period in years.
      discount_rate (float): Discount rate (e.g., WACC), as a decimal (e.g., 0.10 for 10%).
      growth_rate (float): Annual growth rate for free cash flow, as a decimal.
      terminal_growth_rate (float): Perpetual growth rate for terminal value calculation (default: 0.02).

    Returns:
      dict: A dictionary containing:
          - forecast_fcfs: Forecasted free cash flows for each year.
          - discounted_fcfs: Discounted free cash flows for each year.
          - terminal_value: Calculated terminal value.
          - discounted_terminal_value: Discounted terminal value.
          - total_dcf_value: Total enterprise value estimated by the DCF analysis.

    Raises:
      ValueError: If either discount_rate or growth_rate is not provided.
    """
    if discount_rate is None or growth_rate is None:
        raise ValueError("Please provide both discount_rate (WACC) and growth_rate values.")
    
    base_fcf = _get_real_fcf(ticker)
    forecast_fcfs = {}
    discounted_fcfs = {}
    total_discounted_value = 0.0

    # Forecast free cash flow for each year and discount it.
    for i in range(1, years + 1):
        forecast_fcfs[i] = base_fcf * ((1 + growth_rate) ** i)
        discounted_fcfs[i] = forecast_fcfs[i] / ((1 + discount_rate) ** i)
        total_discounted_value += discounted_fcfs[i]

    # Calculate terminal value using the Gordon Growth Model.
    terminal_cash_flow = base_fcf * ((1 + growth_rate) ** years)
    terminal_value = terminal_cash_flow * (1 + terminal_growth_rate) / (discount_rate - terminal_growth_rate)
    discounted_terminal_value = terminal_value / ((1 + discount_rate) ** years)
    total_dcf_value = total_discounted_value + discounted_terminal_value

    return {
        "forecast_fcfs": forecast_fcfs,
        "discounted_fcfs": discounted_fcfs,
        "terminal_value": terminal_value,
        "discounted_terminal_value": discounted_terminal_value,
        "total_dcf_value": total_dcf_value
    }
