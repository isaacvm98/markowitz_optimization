"""
S&P 500 Stock Universe for Portfolio Optimization
Clean, reliable data source for major US companies.
"""

import pandas as pd
import yfinance as yf
import numpy as np

def load_sp500_data():
    """Load S&P 500 tickers from reliable source."""
    url = "https://gist.githubusercontent.com/ZeccaLehn/f6a2613b24c393821f81c0c1d23d4192/raw/fe4638cc5561b9b261225fd8d2a9463a04e77d19/SP500.csv"
    
    df = pd.read_csv(url)
    print(f"Loaded {len(df)} S&P 500 companies")
    print(f"Columns: {list(df.columns)}")
    
    return df

def get_stocks_by_sector(df, sector=None, top_n=20):
    """Get stocks by sector from S&P 500."""
    
    # Map of user-friendly names to exact sector names
    sector_mapping = {
        'tech': 'Information Technology',
        'technology': 'Information Technology',
        'healthcare': 'Health Care',
        'health': 'Health Care',
        'finance': 'Financials',
        'financial': 'Financials',
        'consumer': 'Consumer Discretionary',
        'discretionary': 'Consumer Discretionary',
        'staples': 'Consumer Staples',
        'industrial': 'Industrials',
        'energy': 'Energy',
        'utilities': 'Utilities',
        'materials': 'Materials',
        'realestate': 'Real Estate',
        'real estate': 'Real Estate',
        'telecom': 'Telecommunication Services',
        'communication': 'Telecommunication Services'
    }
    
    if sector:
        # Map user input to exact sector name
        sector_key = sector.lower().replace(' ', '')
        exact_sector = sector_mapping.get(sector_key, sector)
        
        # Filter by specific sector
        sector_stocks = df[df['Sector'] == exact_sector]
        print(f"Found {len(sector_stocks)} stocks in '{exact_sector}' sector")
        
        if len(sector_stocks) == 0:
            print(f"Available sectors: {df['Sector'].unique().tolist()}")
            return []
            
        return sector_stocks['Symbol'].head(top_n).tolist()
    
    else:
        # Diversified selection across sectors
        print("Creating diversified portfolio across all sectors...")
        
        # Get sector distribution
        sector_counts = df['Sector'].value_counts()
        print(f"\nS&P 500 Sector Distribution:")
        for sector, count in sector_counts.items():
            print(f"  {sector:<25}: {count:>3} companies")
        
        # Select stocks from each sector proportionally
        diversified_stocks = []
        stocks_per_sector = max(1, top_n // len(sector_counts))
        
        print(f"\nSelecting ~{stocks_per_sector} stocks per sector:")
        for sector in sector_counts.index:
            sector_stocks = df[df['Sector'] == sector]['Symbol'].head(stocks_per_sector).tolist()
            diversified_stocks.extend(sector_stocks)
            print(f"  {sector:<25}: {sector_stocks}")
        
        return diversified_stocks[:top_n]

def get_stocks_by_market_cap(df, top_n=20):
    """Get largest stocks by market cap."""
    
    print(f"Fetching market cap data for S&P 500 stocks...")
    
    market_cap_data = []
    symbols = df['Symbol'].tolist()
    
    # Process in smaller batches
    batch_size = 25
    for i in range(0, min(len(symbols), 100), batch_size):  # Limit to first 100 for speed
        batch = symbols[i:i+batch_size]
        print(f"Processing batch {i//batch_size + 1}")
        
        for symbol in batch:
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                
                market_cap = info.get('marketCap')
                if market_cap:
                    market_cap_data.append({
                        'Symbol': symbol,
                        'Company': df[df['Symbol'] == symbol]['Name'].iloc[0],
                        'Sector': df[df['Symbol'] == symbol]['Sector'].iloc[0],
                        'MarketCap': market_cap,
                        'MarketCapB': market_cap / 1e9
                    })
                    
            except:
                continue
        
        import time
        time.sleep(0.2)  # Be nice to the API
    
    # Sort by market cap
    market_cap_df = pd.DataFrame(market_cap_data)
    top_stocks = market_cap_df.nlargest(top_n, 'MarketCap')
    
    print(f"\nTop {len(top_stocks)} S&P 500 stocks by market cap:")
    print(f"{'Symbol':<8} {'Market Cap ($B)':<15} {'Sector':<20} {'Company'}")
    print("-" * 80)
    for _, row in top_stocks.head(10).iterrows():
        print(f"{row['Symbol']:<8} {row['MarketCapB']:<15.1f} {row['Sector']:<20} {row['Company'][:30]}")
    
    return top_stocks['Symbol'].tolist()

def analyze_sp500_portfolio():
    """Main analysis function using S&P 500 data."""
    
    print("=== S&P 500 PORTFOLIO ANALYSIS ===")
    
    # Load S&P 500 data
    sp500_df = load_sp500_data()
    sp500_df = sp500_df[sp500_df['Symbol'].isin(['GOOGL','ANSS','ABC', 'AGN', 'ALXN',
                                                 'ANTM','AET','ANDV','ADS', 'ATVI', 'CTL', 'APC','BHGE',
                                                 'COG','CHK'])==False] # Use GOOGL instead
    # Different portfolio selection strategies
    print(f"\n1. Information Technology Sector:")
    tech_stocks = get_stocks_by_sector(sp500_df, 'Information Technology', 12)
    
    print(f"\n2. Health Care Sector:")
    health_stocks = get_stocks_by_sector(sp500_df, 'Health Care', 10)
    
    print(f"\n3. Financials Sector:")
    finance_stocks = get_stocks_by_sector(sp500_df, 'Financials', 8)

    print(f"\n4. Diversified Across All Sectors:")
    diversified_stocks = get_stocks_by_sector(sp500_df, sector=None, top_n=22)  # ~2 per sector
    
    print(f"\n5. Largest by Market Cap:")
    large_cap_stocks = get_stocks_by_market_cap(sp500_df, 15)
    
    return {
        'tech': tech_stocks,
        'healthcare': health_stocks,
        'financials': finance_stocks,
        'diversified': diversified_stocks,
        'large_cap': large_cap_stocks,
        'sp500_df': sp500_df
    }

if __name__ == "__main__":
    portfolios = analyze_sp500_portfolio()
    
    # Example: Use with your portfolio optimizer
    print(f"\n=== READY FOR OPTIMIZATION ===")
    print(f"Tech portfolio: {portfolios['tech']}")
    print(f"Diversified portfolio: {portfolios['diversified']}")
    
    # Now you can use these with your existing optimizer:
    # from data import get_data
    # from optimize import Portfolio
    # 
    # prices, returns = get_data(portfolios['tech'])
    # portfolio = Portfolio(returns)
    # max_sharpe = portfolio.max_sharpe()