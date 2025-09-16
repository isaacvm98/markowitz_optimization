from data_fetch.data_fetcher import get_data, TECH, US
from optimizer import Portfolio

def analyze(name, tickers):
    print(f"\n=== {name} ===")
    
    # Get data
    prices, returns = get_data(tickers)
    portfolio = Portfolio(returns)
    
    # Optimize
    max_sharpe = portfolio.max_sharpe()
    min_vol = portfolio.min_vol()
    
    # Stats
    sharpe_stats = portfolio.stats(max_sharpe)
    vol_stats = portfolio.stats(min_vol)
    
    print(f"Max Sharpe: {sharpe_stats['return']:.1%} return, {sharpe_stats['sharpe']:.2f} Sharpe")
    print(f"Min Vol:    {vol_stats['return']:.1%} return, {vol_stats['volatility']:.1%} volatility")
    
    # Top holdings
    top_sharpe = sorted(max_sharpe.items(), key=lambda x: x[1], reverse=True)[:3]
    print(f"Top holdings: {', '.join([f'{k} ({v:.1%})' for k, v in top_sharpe])}")
    
    return portfolio

if __name__ == "__main__":
    tech_portfolio = analyze("Tech Stocks", TECH)
    us_portfolio = analyze("US Stocks", US)
    
    # Plot efficient frontiers
    print("\nPlotting efficient frontiers...")
    tech_portfolio.plot_frontier()
    us_portfolio.plot_frontier()