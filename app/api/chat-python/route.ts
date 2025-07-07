import { streamText } from "ai"
import { groq } from "@ai-sdk/groq"

export async function POST(req: Request) {
  const { message, portfolioData } = await req.json()

  // Get portfolio context from Python data
  const portfolioContext = portfolioData
    ? `
Current Portfolio Context:
- Total Value: $${portfolioData.total_value?.toLocaleString() || "125,750"}
- Asset Allocation: ${JSON.stringify(portfolioData.asset_allocation || {})}
- Geographic Allocation: ${JSON.stringify(portfolioData.geographic_allocation || {})}
- Risk Profile: ${portfolioData.risk_profile || "moderate"}
- Portfolio Return: ${portfolioData.metrics?.portfolio_return?.toFixed(2) || "N/A"}%
- Sharpe Ratio: ${portfolioData.metrics?.sharpe_ratio?.toFixed(2) || "N/A"}
- Volatility: ${portfolioData.metrics?.portfolio_volatility?.toFixed(1) || "N/A"}%
`
    : ""

  const result = await streamText({
    model: groq("meta-llama/llama-4-maverick-17b-128e-instruct"),
    system: `You are an expert AI Portfolio Manager for QuantAlpha, powered by Python analytics and Groq's Llama model.

${portfolioContext}

Your role:
- Provide intelligent portfolio allocation advice based on the Python-calculated metrics
- Analyze market conditions and their impact on investments  
- Explain investment decisions with clear reasoning
- Consider risk management and diversification
- Reference the specific portfolio data provided

Guidelines:
- Be concise but informative (max 200 words)
- Provide specific actionable advice
- Reference current portfolio metrics when relevant
- Explain the reasoning behind recommendations
- Maintain a professional, confident tone`,
    messages: [{ role: "user", content: message }],
    maxTokens: 500,
  })

  return result.toAIStreamResponse()
}
