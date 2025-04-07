# efin
efin is a comprehensive Python library for financial analysis, valuation, and forecasting. It integrates data retrieval from Yahoo Finance with multiple valuation methods, risk metrics, portfolio analysis, forecasting techniques, caching, visualization, and a command-line interface (CLI). This library is ideal for investors, financial analysts, and researchers looking to quickly prototype and test financial models.

# Features
# Valuation Models
Discounted Cash Flow (DCF) Valuation:
Calculates the intrinsic value of a stock based on user-supplied discount rate (WACC) and growth rate, using real free cash flow (FCF) data from Yahoo Finance.

Real FCF Retrieval: Retrieves FCF from the cash flow statement (using "Free Cash Flow" if available, or computes it from operating cash flow and CAPEX).

Dividend Discount Model (DDM):
Estimates a stock's value based on expected dividend growth.

Comparable Company Analysis:
Compares valuation multiples (e.g., trailing P/E) of a target company against its peers.

Residual Income Model (RIM):
Estimates intrinsic value by discounting forecast residual income (EPS minus cost-of-equity on book value) over a specified period.

# Forecasting
Unified Forecast Function:
Uses a simple linear regression model to forecast future stock prices based on historical adjusted close data.

Grid Search Auto ARIMA Forecast:
Implements an automatic grid search over ARIMA parameters (p, d, q) using statsmodels to select the best ARIMA model based on AIC and forecast future prices.

# Risk Metrics
Volatility Calculation:
Computes the standard deviation of daily returns.

Sharpe Ratio:
Calculates the risk-adjusted return of a stock by comparing excess returns to volatility.

# Portfolio Analysis
Historical Data Aggregation:
Downloads and extracts adjusted close prices for one or more tickers.

Basic Portfolio Optimization:
Provides a simple, equal-weighted portfolio allocation (a placeholder for more advanced methods).

# Data Caching
Efficient Data Retrieval:
Uses caching (via requests_cache) to store and retrieve financial data, reducing API calls and speeding up repeated analyses.

# Visualization
Plotting Functions:
Generate visualizations to compare historical data with forecasted trends.

# Command-Line Interface (CLI)
Interactive CLI:
Run valuations and forecasts from the terminal. The CLI supports multiple forecasting methods:

Linear Forecast: Uses the unified forecast function.

Grid Search ARIMA Forecast: Uses the auto ARIMA grid search function.

# Installation:

pip install efin


# Dependencies:

The library requires:

Python 3.6+:

yfinance
statsmodels
click
requests_cache
matplotlib
numpy
pandas
scikit-learn

# Usage Examples

# Valuation

# Discounted Cash Flow (DCF) Valuation

import efin


#Calculate DCF for AAPL over a 5-year period with a 10% discount rate and 5% growth rate.

dcf_result = efin.dcf("AAPL", years=5, discount_rate=0.10, growth_rate=0.05, terminal_growth_rate=0.02)

print("Total DCF Value:", dcf_result["total_dcf_value"])

# Dividend Discount Model (DDM)

import efin


#Estimate the stock price of KO using a 3% dividend growth rate and a 10% discount rate.

ddm_price = efin.dividend_discount_model("KO", growth_rate=0.03, discount_rate=0.1)

print("DDM Price for KO:", ddm_price)

# Comparable Company Analysis

import efin


#Compare AAPL against MSFT and GOOGL using the trailing P/E multiple.

result = efin.comparable_company_analysis("AAPL", ["MSFT", "GOOGL"], multiple="trailingPE")

print(result)

# Residual Income Model (RIM)

import efin


#Estimate intrinsic value for AAPL using a 10% cost of equity, 5% growth rate, over 5 periods.

rim_value = efin.residual_income_model("AAPL", cost_of_equity=0.10, growth_rate=0.05, forecast_period=5)

print("Residual Income Value:", rim_value)

# Forecasting

# Unified Forecast (Linear Regression)

import efin


#Forecast AAPL prices for the next 30 days using a linear regression approach.

forecast_df = efin.forecast("AAPL", forecast_period=30, start_date="2010-01-01")

print(forecast_df)

# Auto ARIMA Grid Forecast

import efin


#Forecast AAPL prices for the next 5 days using a grid search over ARIMA parameters.

forecast_df, best_order, best_aic = efin.auto_arima_grid_forecast("AAPL", forecast_period=5, start_date="2010-01-01")

print("Best ARIMA order:", best_order, "with AIC:", best_aic)

print(forecast_df)

# Risk Metrics

import efin


#Calculate the volatility and Sharpe ratio for AAPL.

volatility = efin.calculate_volatility("AAPL", start_date="2020-01-01")

sharpe = efin.sharpe_ratio("AAPL", risk_free_rate=0.01, start_date="2020-01-01")

print("Volatility:", volatility)

print("Sharpe Ratio:", sharpe)

# Portfolio Analysis

import efin


#Download adjusted close prices for AAPL and MSFT.

prices = efin.download_adj_close(["AAPL", "MSFT"], start_date="2020-01-01")

print(prices.head())

#Compute a basic equal-weighted portfolio allocation.

returns = prices.pct_change().dropna()

weights = efin.markowitz_portfolio(returns)

print("Portfolio Weights:", weights)

# Data Caching

import efin


#Initialize caching for 1 hour to speed up repeated data retrieval.

efin.initialize_cache(expire_after=3600)

# Visualization

import efin


from efin.visualization import plot_forecast

import pandas as pd

import numpy as np

#Generate sample historical data

dates = pd.date_range("2020-01-01", periods=50)

history = pd.Series(np.random.randn(50).cumsum(), index=dates)

#Generate sample forecast data for 10 days

forecast_dates = pd.date_range("2020-02-20", periods=10)

forecast_values = pd.Series(np.random.randn(10).cumsum(), index=forecast_dates)

plot_forecast(history, forecast_values, title="Historical vs Forecast")

# Command-Line Interface (CLI)
From the terminal, run:

# Calculate DCF valuation for AAPL over 5 years.
python -m efin.cli dcf AAPL --years 5 --discount_rate 0.10 --growth_rate 0.05 --terminal_growth_rate 0.02

# Forecast stock prices for AAPL using linear regression (default).
python -m efin.cli forecast AAPL --model linear --period 30

# Forecast stock prices for AAPL using grid search ARIMA.
python -m efin.cli forecast AAPL --model grid --period 5

# Contributing
Contributions are welcome! If you have suggestions, bug reports, or improvements, please open an issue or submit a pull request on the GitHub repository:https://github.com/ebeirne/efin

# License
This project is licensed under the MIT License. See the LICENSE file for details.

# Contact
For questions or feedback, please contact ethan.g.beirne@gmail.com
