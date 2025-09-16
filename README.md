# Portfolio Optimization

Simple Markowitz portfolio optimization in Python.

## Usage

```python
from data import get_data, TECH
from optimize import Portfolio

# Get stock data
prices, returns = get_data(TECH)

# Optimize portfolio
portfolio = Portfolio(returns)
max_sharpe_weights = portfolio.max_sharpe()
min_vol_weights = portfolio.min_vol()

# Get stats
stats = portfolio.stats(max_sharpe_weights)
print(f"Return: {stats['return']:.1%}")
print(f"Sharpe: {stats['sharpe']:.2f}")
```

## Run example
```bash
python example.py
```

## Files
- `data.py` - Get stock data from yfinance
- `optimize.py` - Markowitz optimization 
- `example.py` - Usage example

## Requirements
```
numpy
scipy
yfinance
```