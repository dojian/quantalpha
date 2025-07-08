import { type NextRequest, NextResponse } from "next/server"
import { exec } from "child_process"
import { promisify } from "util"

const execAsync = promisify(exec)

export async function GET() {
  try {
//   const { stdout } = await execAsync("python scripts/portfolio_manager.py")
//   const portfolioData = JSON.parse(stdout.split("Portfolio Summary:")[0])
      const portfolioData = {"total_value": 125750.52, "assets": [{"symbol": "AAPL", "name": "Apple Inc.", "asset_type": "stock", "region": "US", "allocation": 15.0, "value": 18862.58, "current_price": 185.5, "change_percent": 1.8}, {"symbol": "MSFT", "name": "Microsoft Corp.", "asset_type": "stock", "region": "US", "allocation": 12.0, "value": 15090.06, "current_price": 380.25, "change_percent": 2.4}, {"symbol": "GOOGL", "name": "Alphabet Inc.", "asset_type": "stock", "region": "US", "allocation": 8.0, "value": 10060.04, "current_price": 142.3, "change_percent": -0.8}, {"symbol": "BTC", "name": "Bitcoin", "asset_type": "crypto", "region": "Global", "allocation": 5.0, "value": 6287.53, "current_price": 45200.0, "change_percent": 12.1}, {"symbol": "TLT", "name": "20+ Year Treasury Bond ETF", "asset_type": "bond", "region": "US", "allocation": 15.0, "value": 18862.58, "current_price": 95.4, "change_percent": -0.3}, {"symbol": "VEA", "name": "Developed Markets ETF", "asset_type": "stock", "region": "Developed", "allocation": 20.0, "value": 25150.1, "current_price": 48.75, "change_percent": 1.5}, {"symbol": "VWO", "name": "Emerging Markets ETF", "asset_type": "stock", "region": "Emerging", "allocation": 15.0, "value": 18862.58, "current_price": 42.3, "change_percent": 4.2}, {"symbol": "CASH", "name": "Cash & Equivalents", "asset_type": "cash", "region": "US", "allocation": 10.0, "value": 12575.05, "current_price": 1.0, "change_percent": 0.0}], "risk_profile": "moderate", "last_updated": "2025-07-08T11:26:36.880089", "metrics": {"portfolio_return": 1.984, "portfolio_volatility": 61.84662985967789, "sharpe_ratio": 8.03549039175711, "total_value": 125750.52, "num_assets": 8}, "asset_allocation": {"stock": 70.0, "bond": 15.0, "crypto": 5.0, "cash": 10.0}, "geographic_allocation": {"US": 60.0, "Developed": 20.0, "Emerging": 15.0, "Global": 5.0}}
{'total_value': 125750.52, 'assets': [{'symbol': 'AAPL', 'name': 'Apple Inc.', 'asset_type': 'stock', 'region': 'US', 'allocation': 15.0, 'value': 18862.58, 'current_price': 185.5, 'change_percent': 1.8}, {'symbol': 'MSFT', 'name': 'Microsoft Corp.', 'asset_type': 'stock', 'region': 'US', 'allocation': 12.0, 'value': 15090.06, 'current_price': 380.25, 'change_percent': 2.4}, {'symbol': 'GOOGL', 'name': 'Alphabet Inc.', 'asset_type': 'stock', 'region': 'US', 'allocation': 8.0, 'value': 10060.04, 'current_price': 142.3, 'change_percent': -0.8}, {'symbol': 'BTC', 'name': 'Bitcoin', 'asset_type': 'crypto', 'region': 'Global', 'allocation': 5.0, 'value': 6287.53, 'current_price': 45200.0, 'change_percent': 12.1}, {'symbol': 'TLT', 'name': '20+ Year Treasury Bond ETF', 'asset_type': 'bond', 'region': 'US', 'allocation': 15.0, 'value': 18862.58, 'current_price': 95.4, 'change_percent': -0.3}, {'symbol': 'VEA', 'name': 'Developed Markets ETF', 'asset_type': 'stock', 'region': 'Developed', 'allocation': 20.0, 'value': 25150.1, 'current_price': 48.75, 'change_percent': 1.5}, {'symbol': 'VWO', 'name': 'Emerging Markets ETF', 'asset_type': 'stock', 'region': 'Emerging', 'allocation': 15.0, 'value': 18862.58, 'current_price': 42.3, 'change_percent': 4.2}, {'symbol': 'CASH', 'name': 'Cash & Equivalents', 'asset_type': 'cash', 'region': 'US', 'allocation': 10.0, 'value': 12575.05, 'current_price': 1.0, 'change_percent': 0.0}], 'risk_profile': 'moderate', 'last_updated': '2025-07-08T11:26:36.880089', 'metrics': {'portfolio_return': 1.984, 'portfolio_volatility': np.float64(61.84662985967789), 'sharpe_ratio': np.float64(8.03549039175711), 'total_value': 125750.52, 'num_assets': 8}, 'asset_allocation': {'stock': 70.0, 'bond': 15.0, 'crypto': 5.0, 'cash': 10.0}, 'geographic_allocation': {'US': 60.0, 'Developed': 20.0, 'Emerging': 15.0, 'Global': 5.0}}
    
    return NextResponse.json(portfolioData)
  } catch (error) {
    console.error("Error running Python portfolio script:", error)
    return NextResponse.json({ error: "Internal server error while loading portfolio data." }, { status: 500 })
  }
}

export async function POST(req: NextRequest) {
  try {
    const { action, data } = await req.json()

    let command = ""
    switch (action) {
      case "analyze":
        command = `python scripts/ai_portfolio_advisor.py`
        break
      case "scenario":
        command = `python scripts/scenario_analysis.py`
        break
      case "risk_profile":
        command = `python scripts/risk_profiler.py`
        break
      default:
        return NextResponse.json({ error: "Invalid action" }, { status: 400 })
    }

    const { stdout } = await execAsync(command)
    return NextResponse.json({ result: stdout })
  } catch (error) {
    console.error("Error running Python script:", error)
    return NextResponse.json({ error: "Failed to execute Python script" }, { status: 500 })
  }
}
