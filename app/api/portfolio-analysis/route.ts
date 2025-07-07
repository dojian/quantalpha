import { generateText } from "ai"
import { groq } from "@ai-sdk/groq"

export async function POST(req: Request) {
  const { portfolioData, analysisType } = await req.json()

  const systemPrompt = `You are an expert AI Portfolio Manager using advanced quantitative analysis. Analyze the provided portfolio data and provide specific, actionable insights.

Portfolio Context:
- Total Value: $${portfolioData.totalValue?.toLocaleString() || "125,750"}
- Asset Mix: Stocks, Bonds, Crypto, Cash
- Geographic Diversification: US, Developed, Emerging Markets
- Risk Profile: Moderate

Analysis Type: ${analysisType}

Provide a concise, professional analysis with:
1. Key findings
2. Specific recommendations
3. Risk considerations
4. Market context

Keep response under 200 words and focus on actionable insights.`

  try {
    const { text } = await generateText({
      model: groq("meta-llama/llama-4-maverick-17b-128e-instruct"),
      system: systemPrompt,
      prompt: `Analyze this portfolio data: ${JSON.stringify(portfolioData)}`,
      maxTokens: 500,
    })

    return Response.json({ analysis: text })
  } catch (error) {
    console.error("Portfolio analysis error:", error)
    return Response.json({ error: "Analysis failed" }, { status: 500 })
  }
}
