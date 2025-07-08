import { type NextRequest, NextResponse } from "next/server"
import { exec } from "child_process"
import { promisify } from "util"

const execAsync = promisify(exec)

export async function GET() {
  try {
    const { stdout } = await execAsync("python scripts/portfolio_manager.py")
//    const portfolioData = JSON.parse(stdout.split("Portfolio Summary:")[0])
      const portfolioData = JSON.parse(stdout)
    
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
