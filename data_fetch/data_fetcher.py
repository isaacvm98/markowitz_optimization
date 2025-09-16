import yfinance as yf

def get_data(tickers, start='2020-01-01'):
    """Get stock data and returns."""

    data = yf.download(tickers, start=start,auto_adjust=True)['Close']
    returns = data.pct_change(fill_method=None).dropna()
    return data, returns

# Stock lists
TECH = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META']
US = ['AAPL', 'MSFT', 'JPM', 'JNJ', 'WMT', 'PG', 'V', 'UNH']
MEXICAN = ['WALMEX.MX', 'CEMEXCPO.MX', 'BIMBOA.MX', 'GMEXICOB.MX']