import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from scipy.optimize import minimize

class Portfolio:
    def __init__(self, returns):
        self.returns = returns
        self.assets = list(returns.columns)
        self.mean = returns.mean() * 252  # Annualize
        self.cov = returns.cov() * 252    # Annualize
    
    def max_sharpe(self):
        """Find portfolio with maximum Sharpe ratio."""
        n = len(self.assets)
        
        def neg_sharpe(weights):
            ret = np.dot(weights, self.mean)
            vol = np.sqrt(np.dot(weights, np.dot(self.cov, weights)))
            return -ret / vol  # Negative for minimization
        
        constraints = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
        bounds = [(0, 1) for _ in range(n)]
        guess = [1/n] * n
        
        result = minimize(neg_sharpe, guess, bounds=bounds, constraints=constraints)
        return dict(zip(self.assets, result.x))
    
    def min_vol(self):
        """Find portfolio with minimum volatility."""
        n = len(self.assets)
        
        def volatility(weights):
            return np.sqrt(np.dot(weights, np.dot(self.cov, weights)))
        
        constraints = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
        bounds = [(0, 1) for _ in range(n)]
        guess = [1/n] * n
        
        result = minimize(volatility, guess, bounds=bounds, constraints=constraints)
        return dict(zip(self.assets, result.x))
    
    def stats(self, weights):
        """Get portfolio stats."""
        w = np.array([weights[asset] for asset in self.assets])
        ret = np.dot(w, self.mean)
        vol = np.sqrt(np.dot(w, np.dot(self.cov, w)))
        sharpe = ret / vol
        return {'return': ret, 'volatility': vol, 'sharpe': sharpe}
    
    def efficient_frontier(self, n_points=50):
        """Calculate efficient frontier points."""
        # Get min and max returns
        min_vol_weights = self.min_vol()
        min_ret = self.stats(min_vol_weights)['return']
        max_ret = self.mean.max() * 0.95  # Slightly below single best asset
        
        # Target returns
        target_returns = np.linspace(min_ret, max_ret, n_points)
        
        frontier_vols = []
        frontier_rets = []
        
        for target in target_returns:
            try:
                weights = self._optimize_for_return(target)
                if weights:
                    stats = self.stats(weights)
                    frontier_rets.append(stats['return'])
                    frontier_vols.append(stats['volatility'])
            except:
                continue
        
        return np.array(frontier_vols), np.array(frontier_rets)
    
    def _optimize_for_return(self, target_return):
        """Find min volatility portfolio for target return."""
        n = len(self.assets)
        
        def volatility(weights):
            return np.sqrt(np.dot(weights, np.dot(self.cov, weights)))
        
        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
            {'type': 'eq', 'fun': lambda x: np.dot(x, self.mean) - target_return}
        ]
        bounds = [(0, 1) for _ in range(n)]
        guess = [1/n] * n
        
        result = minimize(volatility, guess, bounds=bounds, constraints=constraints)
        return dict(zip(self.assets, result.x)) if result.success else None
    
    
    def market_cap_weights(self, market_caps):
        """Market cap weighted portfolio (efficient market benchmark)."""
        return market_caps
    
    def equal_weight(self):
        """Equal weight portfolio."""
        n = len(self.assets)
        return {asset: 1/n for asset in self.assets}
    
    def plot_weights(self, weights, title="Portfolio Weights", save=True):
        """Plot portfolio weights as pie chart."""
        # Filter out zero weights
        filtered_weights = {k: v for k, v in weights.items() if v > 0.01}
        
        if not filtered_weights:
            print("No significant weights to plot")
            return
        
        assets = list(filtered_weights.keys())
        values = list(filtered_weights.values())
        
        plt.figure(figsize=(8, 6))
        plt.pie(values, labels=assets, autopct='%1.1f%%', startangle=90)
        plt.title(title)
        plt.axis('equal')
        
        if save:
            filename = f"{title.replace(' ', '_').replace('-', '').lower()}.png"
            plt.savefig(f'visualizations/{filename}', dpi=150, bbox_inches='tight')
            print(f"Saved plot: {filename}")
        else:
            plt.show()
        plt.close()
    
    def plot_frontier(self, save=True,fname=None):
        """Plot efficient frontier."""
        # Calculate frontier
        vols, rets = self.efficient_frontier()
        
        # Get special portfolios
        max_sharpe = self.max_sharpe()
        min_vol = self.min_vol()
        sharpe_stats = self.stats(max_sharpe)
        vol_stats = self.stats(min_vol)
        
        # Plot
        plt.figure(figsize=(10, 6))
        plt.plot(vols, rets, 'b-', linewidth=2, label='Efficient Frontier')
        plt.plot(sharpe_stats['volatility'], sharpe_stats['return'], 'r*', 
                markersize=15, label=f'Max Sharpe ({sharpe_stats["sharpe"]:.2f})')
        plt.plot(vol_stats['volatility'], vol_stats['return'], 'g*', 
                markersize=15, label='Min Volatility')
        
        # Individual assets
        for i, asset in enumerate(self.assets):
            vol = np.sqrt(self.cov.iloc[i, i])
            ret = self.mean.iloc[i]
            plt.plot(vol, ret, 'ko', alpha=0.7)
            plt.annotate(asset, (vol, ret), xytext=(5, 5), 
                        textcoords='offset points', fontsize=9)
        
        plt.xlabel('Volatility')
        plt.ylabel('Expected Return')
        plt.title('Efficient Frontier')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        if save:
            if fname is None:
                fname = 'efficient_frontier.png'
            plt.savefig(f'visualizations/{fname}', dpi=150, bbox_inches='tight')
            print(f"Saved plot: {fname}")
        else:
            plt.show()
        plt.close()
    
    def compare_all(self, market_caps=None):
        """Compare all strategies."""
        strategies = {
            'Equal Weight': self.equal_weight(),
            'Max Sharpe': self.max_sharpe(),
            'Min Volatility': self.min_vol()
        }
        
        if market_caps:
            strategies['Market Cap'] = self.market_cap_weights(market_caps)
        
        print(f"{'Strategy':<15} | {'Return':<8} | {'Vol':<8} | {'Sharpe':<6}")
        print("-" * 50)
        
        for name, weights in strategies.items():
            stats = self.stats(weights)
            print(f"{name:<15} | {stats['return']:>6.1%} | {stats['volatility']:>6.1%} | {stats['sharpe']:>6.2f}")
        
        return strategies