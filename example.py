from data_fetch.data_fetcher import get_data, get_market_caps, TECH, US
from optimizer import Portfolio

def analyze(name, tickers):
    print(f"\n=== {name} ===")
    
    # Get data
    prices, returns = get_data(tickers)
    market_caps = get_market_caps(tickers)
    portfolio = Portfolio(returns)
    
    # Compare all strategies
    strategies = portfolio.compare_all(market_caps)
    
    # Show pie charts for best strategies
    max_sharpe = strategies['Max Sharpe']
    market_cap = strategies['Market Cap']
    
    print(f"\nTop Max Sharpe holdings:")
    top_holdings = sorted(max_sharpe.items(), key=lambda x: x[1], reverse=True)[:3]
    for asset, weight in top_holdings:
        print(f"  {asset}: {weight:.1%}")
    
    return portfolio, strategies

if __name__ == "__main__":
    tech_portfolio, tech_strategies = analyze("Tech Stocks", TECH)
    us_portfolio, us_strategies = analyze("US Stocks", US)
    
    # Plot pie charts
    print("\nShowing portfolio allocations...")
    tech_portfolio.plot_weights(tech_strategies['Max Sharpe'], "Tech - Max Sharpe Portfolio")
    tech_portfolio.plot_weights(tech_strategies['Market Cap'], "Tech - Market Cap Weights")
    
    # Plot efficient frontier
    print("\nShowing efficient frontier...")
    tech_portfolio.plot_frontier()