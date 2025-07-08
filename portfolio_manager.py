import os
import json
from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime
import numpy as np
import pandas as pd

@dataclass
class Asset:
    symbol: str
    name: str
    asset_type: str  # 'stock', 'bond', 'crypto', 'cash'
    region: str  # 'US', 'Developed', 'Emerging'
    allocation: float
    value: float
    current_price: float
    change_percent: float

@dataclass
class Portfolio:
    total_value: float
    assets: List[Asset]
    risk_profile: str
    last_updated: datetime

class PortfolioManager:
    def __init__(self):
        self.portfolio = self._initialize_portfolio()
    
    def _initialize_portfolio(self) -> Portfolio:
        """Initialize a sample portfolio"""
        assets = [
            Asset("AAPL", "Apple Inc.", "stock", "US", 15.0, 18862.58, 185.50, 1.8),
            Asset("MSFT", "Microsoft Corp.", "stock", "US", 12.0, 15090.06, 380.25, 2.4),
            Asset("GOOGL", "Alphabet Inc.", "stock", "US", 8.0, 10060.04, 142.30, -0.8),
            Asset("BTC", "Bitcoin", "crypto", "Global", 5.0, 6287.53, 45200.00, 12.1),
            Asset("TLT", "20+ Year Treasury Bond ETF", "bond", "US", 15.0, 18862.58, 95.40, -0.3),
            Asset("VEA", "Developed Markets ETF", "stock", "Developed", 20.0, 25150.10, 48.75, 1.5),
            Asset("VWO", "Emerging Markets ETF", "stock", "Emerging", 15.0, 18862.58, 42.30, 4.2),
            Asset("CASH", "Cash & Equivalents", "cash", "US", 10.0, 12575.05, 1.0, 0.0),
        ]
        
        total_value = sum(asset.value for asset in assets)
        
        return Portfolio(
            total_value=total_value,
            assets=assets,
            risk_profile="moderate",
            last_updated=datetime.now()
        )
    
    def get_asset_allocation(self) -> Dict[str, float]:
        """Get allocation by asset type"""
        allocation = {"stock": 0, "bond": 0, "crypto": 0, "cash": 0}
        
        for asset in self.portfolio.assets:
            allocation[asset.asset_type] += asset.allocation
            
        return allocation
    
    def get_geographic_allocation(self) -> Dict[str, float]:
        """Get allocation by geographic region"""
        allocation = {"US": 0, "Developed": 0, "Emerging": 0, "Global": 0}
        
        for asset in self.portfolio.assets:
            allocation[asset.region] += asset.allocation
            
        return allocation
    
    def calculate_portfolio_metrics(self) -> Dict[str, Any]:
        """Calculate key portfolio metrics"""
        returns = [asset.change_percent for asset in self.portfolio.assets]
        weights = [asset.allocation / 100 for asset in self.portfolio.assets]
        
        # Portfolio return
        portfolio_return = sum(r * w for r, w in zip(returns, weights))
        
        # Portfolio volatility (simplified)
        portfolio_volatility = np.std(returns) * np.sqrt(252)  # Annualized
        
        # Sharpe ratio (assuming 3% risk-free rate)
        risk_free_rate = 3.0
        sharpe_ratio = (portfolio_return * 252 - risk_free_rate) / portfolio_volatility if portfolio_volatility > 0 else 0
        
        return {
            "portfolio_return": portfolio_return,
            "portfolio_volatility": portfolio_volatility,
            "sharpe_ratio": sharpe_ratio,
            "total_value": self.portfolio.total_value,
            "num_assets": len(self.portfolio.assets)
        }
    
    def rebalance_portfolio(self, target_allocation: Dict[str, float]) -> Dict[str, Any]:
        """Rebalance portfolio to target allocation"""
        current_allocation = self.get_asset_allocation()
        
        rebalancing_actions = []
        for asset_type, target_pct in target_allocation.items():
            current_pct = current_allocation.get(asset_type, 0)
            difference = target_pct - current_pct
            
            if abs(difference) > 1.0:  # Only rebalance if difference > 1%
                action = "increase" if difference > 0 else "decrease"
                rebalancing_actions.append({
                    "asset_type": asset_type,
                    "action": action,
                    "current_allocation": current_pct,
                    "target_allocation": target_pct,
                    "difference": difference
                })
        
        return {
            "rebalancing_needed": len(rebalancing_actions) > 0,
            "actions": rebalancing_actions,
            "current_allocation": current_allocation,
            "target_allocation": target_allocation
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert portfolio to dictionary for JSON serialization"""
        return {
            "total_value": self.portfolio.total_value,
            "assets": [
                {
                    "symbol": asset.symbol,
                    "name": asset.name,
                    "asset_type": asset.asset_type,
                    "region": asset.region,
                    "allocation": asset.allocation,
                    "value": asset.value,
                    "current_price": asset.current_price,
                    "change_percent": asset.change_percent
                }
                for asset in self.portfolio.assets
            ],
            "risk_profile": self.portfolio.risk_profile,
            "last_updated": self.portfolio.last_updated.isoformat(),
            "metrics": self.calculate_portfolio_metrics(),
            "asset_allocation": self.get_asset_allocation(),
            "geographic_allocation": self.get_geographic_allocation()
        }

if __name__ == "__main__":
    # Test the portfolio manager
    pm = PortfolioManager()
    portfolio_data = pm.to_dict()

    # 1️⃣  Emit machine-readable JSON for the API route
    print(json.dumps(portfolio_data))

    # 2️⃣  Human-readable summary follows
    print("\nPortfolio Summary:")
    print(f"Total Value: ${portfolio_data['total_value']:,.2f}")
    print(f"Number of Assets: {len(portfolio_data['assets'])}")
    print(f"Asset Allocation: {portfolio_data['asset_allocation']}")
    print(f"Geographic Allocation: {portfolio_data['geographic_allocation']}")
    print(f"Portfolio Metrics: {portfolio_data['metrics']}")
