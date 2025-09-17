import yfinance as yf
import pandas as pd

def get_data(tickers, start='2020-01-01'):
    """Get stock data and returns."""
    data = yf.download(tickers, start=start,auto_adjust=True)['Close']
    returns = data.pct_change(fill_method=None).dropna()
    return data, returns

def get_market_caps(tickers):
    """Get market capitalizations for tickers."""
    market_caps = {}
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            market_caps[ticker] = info.get('marketCap', 1e9)  # Default 1B if missing
        except:
            market_caps[ticker] = 1e9  # Fallback
    
    # Convert to weights
    total_cap = sum(market_caps.values())
    return {ticker: cap/total_cap for ticker, cap in market_caps.items()}

# Stock lists
TECH = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META']
US = ['AAPL', 'MSFT', 'JPM', 'JNJ', 'WMT', 'PG', 'V', 'UNH']
MEXICAN = ['WALMEX.MX', 'CEMEXCPO.MX', 'BIMBOA.MX', 'GMEXICOB.MX']