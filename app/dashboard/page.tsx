"use client"
import { useChat } from "ai/react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import {
  TrendingUp,
  DollarSign,
  PieChart,
  Brain,
  Send,
  ArrowUpRight,
  ArrowDownRight,
  Activity,
  Bell,
  Settings,
  Loader2,
} from "lucide-react"
import ScenarioAnalysis from "@/components/scenario-analysis"
import Link from "next/link"

export default function Dashboard() {
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
    api: "/api/chat",
    initialMessages: [
      {
        id: "1",
        role: "assistant",
        content:
          "Hello! I'm your AI Portfolio Manager powered by Groq's Llama model. I've analyzed your current portfolio and market conditions. Your balanced allocation of 65% stocks, 25% bonds, and 7% crypto is well-positioned for the current market environment. How can I help optimize your investments today?",
      },
    ],
  })

  const portfolioData = {
    totalValue: 125750.5,
    dailyChange: 2847.32,
    dailyChangePercent: 2.31,
    assetAllocation: [
      { type: "Stocks", allocation: 65, value: 81737.83, change: 2.8 },
      { type: "Bonds", allocation: 25, value: 31437.63, change: 0.5 },
      { type: "Crypto", allocation: 7, value: 8802.54, change: 8.2 },
      { type: "Cash", allocation: 3, value: 3772.51, change: 0.0 },
    ],
    geoAllocation: [
      { region: "US Markets", allocation: 55, value: 69162.78, change: 2.1 },
      { region: "Developed Markets", allocation: 30, value: 37725.15, change: 1.8 },
      { region: "Emerging Markets", allocation: 15, value: 18862.58, change: 4.2 },
    ],
    stockAllocations: [
      {
        symbol: "AAPL",
        name: "Apple Inc.",
        allocation: 15,
        value: 18862.58,
        change: 1.8,
        reason: "Strong Q4 earnings beat expectations, iPhone 15 sales momentum",
      },
      {
        symbol: "MSFT",
        name: "Microsoft Corp.",
        allocation: 12,
        value: 15090.06,
        change: 2.4,
        reason: "Azure growth acceleration, AI integration driving revenue",
      },
      {
        symbol: "GOOGL",
        name: "Alphabet Inc.",
        allocation: 8,
        value: 10060.04,
        change: -0.8,
        reason: "Search dominance stable, cloud growth offsetting ad headwinds",
      },
      {
        symbol: "BTC",
        name: "Bitcoin",
        allocation: 5,
        value: 6287.53,
        change: 12.1,
        reason: "Institutional adoption increasing, ETF inflows positive",
      },
      {
        symbol: "TLT",
        name: "20+ Year Treasury Bond ETF",
        allocation: 15,
        value: 18862.58,
        change: -0.3,
        reason: "Duration hedge against rate cuts, yield curve positioning",
      },
      {
        symbol: "VEA",
        name: "Developed Markets ETF",
        allocation: 20,
        value: 25150.1,
        change: 1.5,
        reason: "European recovery momentum, currency tailwinds",
      },
      {
        symbol: "VWO",
        name: "Emerging Markets ETF",
        allocation: 15,
        value: 18862.58,
        change: 4.2,
        reason: "China reopening benefits, commodity exposure",
      },
    ],
  }

  const recentNews = [
    { title: "Apple Reports Record Q4 Revenue", impact: "positive", time: "2h ago" },
    { title: "Fed Signals Potential Rate Cut", impact: "positive", time: "4h ago" },
    { title: "Tech Earnings Season Begins", impact: "neutral", time: "6h ago" },
    { title: "Oil Prices Surge on Supply Concerns", impact: "negative", time: "8h ago" },
  ]

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <header className="bg-white border-b border-slate-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
              <TrendingUp className="w-5 h-5 text-white" />
            </div>
            <h1 className="text-2xl font-bold text-slate-900">QuantAlpha</h1>
            <Badge variant="outline" className="text-xs">
              Powered by Groq Llama
            </Badge>
          </div>
          <div className="flex items-center space-x-4">
            <Button variant="ghost" asChild>
              <Link href="/risk-profile">Risk Profile</Link>
            </Button>
            <Button variant="ghost" size="icon">
              <Bell className="w-5 h-5" />
            </Button>
            <Button variant="ghost" size="icon">
              <Settings className="w-5 h-5" />
            </Button>
            <Avatar>
              <AvatarImage src="/placeholder-user.jpg" />
              <AvatarFallback>JD</AvatarFallback>
            </Avatar>
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Main Content */}
        <div className="flex-1 p-6">
          {/* Portfolio Overview */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Total Portfolio Value</CardTitle>
                <DollarSign className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">${portfolioData.totalValue.toLocaleString()}</div>
                <div className="flex items-center text-sm text-green-600">
                  <ArrowUpRight className="w-4 h-4 mr-1" />
                  +${portfolioData.dailyChange.toLocaleString()} ({portfolioData.dailyChangePercent}%)
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">AI Confidence</CardTitle>
                <Brain className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">94%</div>
                <Progress value={94} className="mt-2" />
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Active Positions</CardTitle>
                <PieChart className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">8</div>
                <p className="text-xs text-muted-foreground">Across 7 sectors</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Risk Score</CardTitle>
                <Activity className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">Medium</div>
                <p className="text-xs text-muted-foreground">Balanced growth</p>
              </CardContent>
            </Card>
          </div>

          <Tabs defaultValue="portfolio" className="space-y-6">
            <TabsList>
              <TabsTrigger value="portfolio">Portfolio</TabsTrigger>
              <TabsTrigger value="scenarios">Scenarios</TabsTrigger>
              <TabsTrigger value="analysis">AI Analysis</TabsTrigger>
              <TabsTrigger value="news">Market News</TabsTrigger>
            </TabsList>

            <TabsContent value="portfolio">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
                <Card>
                  <CardHeader>
                    <CardTitle>Asset Allocation</CardTitle>
                    <CardDescription>Diversified across asset classes</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {portfolioData.assetAllocation.map((asset) => (
                        <div key={asset.type} className="flex items-center justify-between">
                          <div className="flex items-center space-x-3">
                            <div className="w-3 h-3 rounded-full bg-blue-500"></div>
                            <span className="font-medium">{asset.type}</span>
                          </div>
                          <div className="text-right">
                            <div className="font-semibold">{asset.allocation}%</div>
                            <div className="text-sm text-muted-foreground">${asset.value.toLocaleString()}</div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle>Geographic Allocation</CardTitle>
                    <CardDescription>Global market exposure</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {portfolioData.geoAllocation.map((geo) => (
                        <div key={geo.region} className="flex items-center justify-between">
                          <div className="flex items-center space-x-3">
                            <div className="w-3 h-3 rounded-full bg-green-500"></div>
                            <span className="font-medium">{geo.region}</span>
                          </div>
                          <div className="text-right">
                            <div className="font-semibold">{geo.allocation}%</div>
                            <div className="text-sm text-muted-foreground">${geo.value.toLocaleString()}</div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </div>

              <Card>
                <CardHeader>
                  <CardTitle>Detailed Holdings</CardTitle>
                  <CardDescription>Individual positions and AI reasoning</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {portfolioData.stockAllocations.map((position) => (
                      <div key={position.symbol} className="flex items-center justify-between p-4 border rounded-lg">
                        <div className="flex items-center space-x-4">
                          <div className="w-12 h-12 bg-slate-100 rounded-full flex items-center justify-center">
                            <span className="font-semibold text-sm">{position.symbol}</span>
                          </div>
                          <div>
                            <h3 className="font-semibold">{position.name}</h3>
                            <p className="text-sm text-muted-foreground">{position.reason}</p>
                          </div>
                        </div>
                        <div className="text-right">
                          <div className="font-semibold">{position.allocation}%</div>
                          <div className="text-sm text-muted-foreground">${position.value.toLocaleString()}</div>
                          <div
                            className={`text-sm flex items-center ${position.change >= 0 ? "text-green-600" : "text-red-600"}`}
                          >
                            {position.change >= 0 ? (
                              <ArrowUpRight className="w-3 h-3 mr-1" />
                            ) : (
                              <ArrowDownRight className="w-3 h-3 mr-1" />
                            )}
                            {Math.abs(position.change)}%
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="scenarios">
              <ScenarioAnalysis />
            </TabsContent>

            <TabsContent value="analysis">
              <Card>
                <CardHeader>
                  <CardTitle>AI Portfolio Analysis</CardTitle>
                  <CardDescription>Latest insights from your Groq-powered AI portfolio manager</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-6">
                    <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                      <h3 className="font-semibold text-blue-900 mb-2">Market Sentiment Analysis</h3>
                      <p className="text-blue-800">
                        Current market sentiment is cautiously optimistic. Tech earnings are driving positive momentum,
                        while geopolitical tensions create some uncertainty. Our AI recommends maintaining current tech
                        exposure while keeping cash reserves for opportunities.
                      </p>
                    </div>
                    <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
                      <h3 className="font-semibold text-green-900 mb-2">Earnings Impact Assessment</h3>
                      <p className="text-green-800">
                        Apple and Microsoft's strong earnings reports validate our overweight positions. The Llama model
                        analysis shows continued strength in cloud computing and AI-driven revenue streams across our
                        tech holdings.
                      </p>
                    </div>
                    <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                      <h3 className="font-semibold text-yellow-900 mb-2">Risk Assessment</h3>
                      <p className="text-yellow-800">
                        Portfolio beta is 1.15, indicating moderate volatility. The AI model suggests our geographic
                        diversification (55% US, 45% international) provides good risk mitigation against regional
                        market downturns.
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="news">
              <Card>
                <CardHeader>
                  <CardTitle>Market News Impact</CardTitle>
                  <CardDescription>AI-analyzed news affecting your portfolio</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {recentNews.map((news, index) => (
                      <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
                        <div className="flex items-center space-x-4">
                          <Badge
                            variant={
                              news.impact === "positive"
                                ? "default"
                                : news.impact === "negative"
                                  ? "destructive"
                                  : "secondary"
                            }
                          >
                            {news.impact}
                          </Badge>
                          <div>
                            <h3 className="font-semibold">{news.title}</h3>
                            <p className="text-sm text-muted-foreground">{news.time}</p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>

        {/* AI Chat Sidebar */}
        <div className="w-96 border-l border-slate-200 bg-white">
          <div className="p-4 border-b border-slate-200">
            <h2 className="font-semibold flex items-center">
              <Brain className="w-5 h-5 mr-2 text-blue-500" />
              AI Portfolio Manager
            </h2>
            <p className="text-xs text-muted-foreground mt-1">Powered by Groq Llama 3.1</p>
          </div>
          <ScrollArea className="h-[calc(100vh-200px)] p-4">
            <div className="space-y-4">
              {messages.map((message) => (
                <div key={message.id} className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}>
                  <div
                    className={`max-w-[80%] p-3 rounded-lg ${
                      message.role === "user" ? "bg-blue-500 text-white" : "bg-slate-100 text-slate-900"
                    }`}
                  >
                    {message.content}
                  </div>
                </div>
              ))}
              {isLoading && (
                <div className="flex justify-start">
                  <div className="bg-slate-100 text-slate-900 p-3 rounded-lg flex items-center space-x-2">
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>AI is analyzing...</span>
                  </div>
                </div>
              )}
            </div>
          </ScrollArea>
          <div className="p-4 border-t border-slate-200">
            <form onSubmit={handleSubmit} className="flex space-x-2">
              <Input
                placeholder="Ask about your portfolio..."
                value={input}
                onChange={handleInputChange}
                disabled={isLoading}
              />
              <Button type="submit" size="icon" disabled={isLoading}>
                {isLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
              </Button>
            </form>
          </div>
        </div>
      </div>
    </div>
  )
}
