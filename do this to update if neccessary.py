import yfinance as yf

data = yf.Ticker("AAPL")
print(data.cashflow)
