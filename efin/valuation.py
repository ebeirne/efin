import yfinance as yf
import logging

logger = logging.getLogger(__name__)

def dividend_discount_model(ticker, growth_rate, discount_rate):
    """
    Estimate a stock's value using the Dividend Discount Model (DDM).

    The DDM assumes dividends grow at a constant rate:
         Price = D1 / (r - g)
    where D1 is the expected dividend next period, r is the discount rate,
    and g is the dividend growth rate.

    Parameters:
      ticker (str): Stock ticker symbol (e.g., "AAPL").
      growth_rate (float): Expected annual dividend growth rate (e.g., 0.03 for 3%).
      discount_rate (float): Required rate of return (e.g., 0.1 for 10%).

    Returns:
      float: Estimated stock price based on the DDM.

    Raises:
      ValueError: If no dividend data is available.
    """
    try:
        ticker_obj = yf.Ticker(ticker)
        dividends = ticker_obj.dividends
        if dividends.empty:
            raise ValueError(f"No dividend data available for {ticker}.")
        last_dividend = dividends.iloc[-1]
        # Use user-supplied growth rate to forecast next dividend.
        next_dividend = last_dividend * (1 + growth_rate)
        price = next_dividend / (discount_rate - growth_rate)
        return price
    except Exception as e:
        logger.error(f"DDM error for {ticker}: {e}")
        raise

def comparable_company_analysis(target_ticker, peer_tickers, multiple="trailingPE"):
    """
    Perform a simple Comparable Company Analysis based on valuation multiples.

    This function fetches the specified multiple (e.g., trailingPE) for the target company 
    and a list of peer companies, then compares the target's multiple to the average of peers.

    Parameters:
      target_ticker (str): The target company ticker (e.g., "AAPL").
      peer_tickers (list): A list of peer company tickers.
      multiple (str): The valuation multiple to compare (default "trailingPE").

    Returns:
      dict: Contains the target's multiple, the average peer multiple, and an interpretation 
            (undervalued or overvalued).

    Raises:
      ValueError: If required multiple data is missing.
    """
    try:
        target_info = yf.Ticker(target_ticker).info
        target_multiple = target_info.get(multiple)
        if target_multiple is None:
            raise ValueError(f"Target multiple '{multiple}' not available for {target_ticker}.")

        peer_multiples = []
        for ticker in peer_tickers:
            info = yf.Ticker(ticker).info
            m = info.get(multiple)
            if m is not None:
                peer_multiples.append(m)
        if not peer_multiples:
            raise ValueError("No peer multiples available.")
        avg_peer_multiple = sum(peer_multiples) / len(peer_multiples)
        interpretation = "undervalued" if target_multiple < avg_peer_multiple else "overvalued"
        return {
            "target_ticker": target_ticker,
            "target_multiple": target_multiple,
            "avg_peer_multiple": avg_peer_multiple,
            "interpretation": interpretation
        }
    except Exception as e:
        logger.error(f"Comparable analysis error for {target_ticker}: {e}")
        raise

def residual_income_model(ticker, cost_of_equity, growth_rate, forecast_period):
    """
    Estimate a stock's intrinsic value using the Residual Income Model (RIM).

    The model calculates value as:
         Value = Book Value + Sum of discounted residual income,
    where Residual Income is approximated as:
         Residual Income = EPS - (Book Value * cost_of_equity)

    Parameters:
      ticker (str): Stock ticker symbol (e.g., "AAPL").
      cost_of_equity (float): Required return on equity (e.g., 0.1 for 10%).
      growth_rate (float): Expected growth rate in residual income (e.g., 0.05 for 5%).
      forecast_period (int): Number of periods to forecast residual income.

    Returns:
      float: Estimated intrinsic value per share.

    Raises:
      ValueError: If required financial data (book value or EPS) is missing.
    """
    try:
        ticker_obj = yf.Ticker(ticker)
        info = ticker_obj.info
        book_value = info.get("bookValue")
        eps = info.get("trailingEps")
        if book_value is None or eps is None:
            raise ValueError("Required financial metrics (bookValue, trailingEps) are not available.")
        # Initial residual income
        residual = eps - (book_value * cost_of_equity)
        ri_sum = 0.0
        for i in range(1, forecast_period + 1):
            discounted_ri = residual / ((1 + cost_of_equity) ** i)
            ri_sum += discounted_ri
            residual *= (1 + growth_rate)
        intrinsic_value = book_value + ri_sum
        return intrinsic_value
    except Exception as e:
        logger.error(f"Residual income model error for {ticker}: {e}")
        raise
