import os
import json
from typing import Dict, List, Any, Optional
from groq import Groq
from dotenv import load_dotenv
from .portfolio_manager import PortfolioManager

#test

# Load environment variables from .env file
load_dotenv()

class AIPortfolioAdvisor:
    """
    AI-powered portfolio advisor using Groq's Llama models.
    
    Provides intelligent investment advice, portfolio analysis, and market insights
    based on real-time portfolio data and advanced AI reasoning.
    """
    
    def __init__(self):
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        if not self.groq_api_key:
            raise ValueError(
                "GROQ_API_KEY not found in environment variables. "
                "Please check your .env file or run: poetry install && poetry shell"
            )
        
        self.client = Groq(api_key=self.groq_api_key)
        self.portfolio_manager = PortfolioManager()
        
    def _make_groq_request(
        self, 
        messages: List[Dict], 
        max_tokens: int = 1000, 
        stream: bool = False,
        temperature: float = 0.7
    ) -> str:
        """Make a request to Groq API using the official client"""
        try:
            completion = self.client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=messages,
                temperature=temperature,
                max_completion_tokens=max_tokens,
                top_p=1,
                stream=stream,
                stop=None,
            )
            
            if stream:
                # Handle streaming response
                response_text = ""
                for chunk in completion:
                    if chunk.choices[0].delta.content:
                        response_text += chunk.choices[0].delta.content
                return response_text
            else:
                # Handle non-streaming response
                return completion.choices[0].message.content
                
        except Exception as e:
            return f"Error getting AI response: {str(e)}"
    
    def get_portfolio_analysis(self, analysis_type: str = "comprehensive") -> str:
        """
        Get comprehensive AI analysis of the current portfolio.
        
        Args:
            analysis_type: Type of analysis ('comprehensive', 'risk', 'performance', 'allocation')
            
        Returns:
            Detailed portfolio analysis and recommendations
        """
        portfolio_data = self.portfolio_manager.to_dict()
        
        system_prompt = """You are an expert investment portfolio manager AI with deep expertise in:
- Modern Portfolio Theory and quantitative analysis
- Risk management and diversification strategies  
- Market analysis and economic trends
- Asset allocation optimization
- Behavioral finance and client psychology

Your role is to provide professional, actionable investment advice based on rigorous analysis of portfolio data, market conditions, and client objectives. Always maintain a fiduciary standard and act in the client's best interest."""
        
        user_prompt = f"""
        **PORTFOLIO ANALYSIS REQUEST**
        
        **Client Portfolio Summary:**
        • Total Value: ${portfolio_data['total_value']:,.2f}
        • Risk Profile: {portfolio_data['risk_profile'].title()}
        • Last Updated: {portfolio_data['last_updated']}
        • Number of Holdings: {portfolio_data['metrics']['num_assets']}
        
        **Current Asset Allocation:**
        • Equities: {portfolio_data['asset_allocation']['stock']}%
        • Fixed Income: {portfolio_data['asset_allocation']['bond']}%
        • Cryptocurrency: {portfolio_data['asset_allocation']['crypto']}%
        • Cash & Equivalents: {portfolio_data['asset_allocation']['cash']}%
        
        **Geographic Diversification:**
        • US Markets: {portfolio_data['geographic_allocation']['US']}%
        • Developed International: {portfolio_data['geographic_allocation']['Developed']}%
        • Emerging Markets: {portfolio_data['geographic_allocation']['Emerging']}%
        • Global/Other: {portfolio_data['geographic_allocation'].get('Global', 0)}%
        
        **Performance Metrics:**
        • Portfolio Return: {portfolio_data['metrics']['portfolio_return']:.2f}%
        • Annualized Volatility: {portfolio_data['metrics']['portfolio_volatility']:.2f}%
        • Sharpe Ratio: {portfolio_data['metrics']['sharpe_ratio']:.2f}
        
        **Analysis Focus: {analysis_type.title()}**
        
        Please provide a professional analysis covering:
        1. **Portfolio Health Assessment** - Overall evaluation of current allocation
        2. **Risk-Return Profile** - Analysis of risk-adjusted performance
        3. **Diversification Review** - Assessment of concentration and correlation risks
        4. **Optimization Opportunities** - Specific recommendations for improvement
        5. **Action Items** - Prioritized next steps with rationale
        
        Keep response professional, data-driven, and under 400 words.
        """
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        return self._make_groq_request(messages, max_tokens=1000, temperature=0.6)
    
    def get_rebalancing_advice(self, target_allocation: Dict[str, float]) -> str:
        """Get AI advice on portfolio rebalancing"""
        rebalancing_data = self.portfolio_manager.rebalance_portfolio(target_allocation)
        
        system_prompt = """You are an expert portfolio manager AI specializing in portfolio rebalancing and optimization. Provide clear, actionable advice on portfolio adjustments based on the rebalancing analysis provided."""
        
        user_prompt = f"""
        **Portfolio Rebalancing Analysis**
        
        {json.dumps(rebalancing_data, indent=2)}
        
        Based on this rebalancing analysis, please provide specific advice on:
        1. Whether rebalancing is recommended at this time
        2. Which specific assets to buy or sell
        3. Optimal timing considerations for these trades
        4. Risk implications of the proposed changes
        5. Expected impact on portfolio performance
        
        Keep your response concise and actionable.
        """
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        return self._make_groq_request(messages, max_tokens=600)
    
    def get_market_outlook(self) -> str:
        """Get AI market outlook and portfolio implications"""
        portfolio_data = self.portfolio_manager.to_dict()
        
        system_prompt = """You are a senior investment strategist AI with expertise in market analysis and portfolio management. Provide market outlook and specific implications for the given portfolio based on current market conditions and trends."""
        
        user_prompt = f"""
        **Portfolio Market Exposure Analysis**
        
        **Current Portfolio Allocation:**
        - Equity Exposure: {portfolio_data['asset_allocation']['stock']}%
        - Fixed Income: {portfolio_data['asset_allocation']['bond']}%
        - Alternative Assets (Crypto): {portfolio_data['asset_allocation']['crypto']}%
        - Cash Position: {portfolio_data['asset_allocation']['cash']}%
        
        **Geographic Distribution:**
        - US Markets: {portfolio_data['geographic_allocation']['US']}%
        - International Developed: {portfolio_data['geographic_allocation']['Developed']}%
        - Emerging Markets: {portfolio_data['geographic_allocation']['Emerging']}%
        
        **Portfolio Characteristics:**
        - Risk Profile: {portfolio_data['risk_profile']}
        - Current Volatility: {portfolio_data['metrics']['portfolio_volatility']:.1f}%
        - Sharpe Ratio: {portfolio_data['metrics']['sharpe_ratio']:.2f}
        
        Please provide:
        1. Current market outlook and key trends
        2. Risks and opportunities for this specific portfolio
        3. Sector or geographic allocation adjustments if needed
        4. Timeline considerations for any recommended changes
        
        Focus on actionable insights relevant to this portfolio's composition.
        """
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        return self._make_groq_request(messages, max_tokens=700)
    
    def chat_with_advisor(
        self, 
        user_message: str, 
        conversation_history: Optional[List[Dict]] = None
    ) -> str:
        """
        Interactive chat with AI portfolio advisor.
        
        Args:
            user_message: User's question or request
            conversation_history: Previous conversation messages for context
            
        Returns:
            AI advisor's response with portfolio-specific insights
        """
        portfolio_data = self.portfolio_manager.to_dict()
        
        system_prompt = f"""You are a senior AI Portfolio Manager for QuantAlpha with expertise in quantitative finance and investment strategy.

**CURRENT CLIENT PORTFOLIO:**
• Value: ${portfolio_data['total_value']:,.2f} | Risk: {portfolio_data['risk_profile']}
• Allocation: {portfolio_data['asset_allocation']['stock']}% stocks, {portfolio_data['asset_allocation']['bond']}% bonds, {portfolio_data['asset_allocation']['crypto']}% crypto, {portfolio_data['asset_allocation']['cash']}% cash
• Geography: {portfolio_data['geographic_allocation']['US']}% US, {portfolio_data['geographic_allocation']['Developed']}% developed, {portfolio_data['geographic_allocation']['Emerging']}% emerging
• Performance: {portfolio_data['metrics']['portfolio_return']:.1f}% return, {portfolio_data['metrics']['sharpe_ratio']:.2f} Sharpe, {portfolio_data['metrics']['portfolio_volatility']:.1f}% volatility

**YOUR EXPERTISE:**
- Portfolio optimization and rebalancing strategies
- Risk management and downside protection
- Market analysis and sector rotation
- Tax-efficient investing and asset location
- Behavioral coaching and investment discipline

**COMMUNICATION STYLE:**
- Professional yet approachable
- Data-driven with clear reasoning
- Specific and actionable recommendations
- Reference client's actual portfolio when relevant
- Concise responses (under 200 words)

Always consider the client's current allocation, risk profile, and performance metrics when providing advice."""
        
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history (keep last 6 messages for context)
        if conversation_history:
            messages.extend(conversation_history[-6:])
        
        messages.append({"role": "user", "content": user_message})
        
        return self._make_groq_request(messages, max_tokens=500, temperature=0.7)
    
    def stream_chat_response(self, user_message: str, conversation_history: List[Dict] = None):
        """Stream chat response for real-time interaction"""
        portfolio_data = self.portfolio_manager.to_dict()
        
        system_prompt = f"""You are an expert AI Portfolio Manager for QuantAlpha.

**Client Portfolio:** ${portfolio_data['total_value']:,.2f} | {portfolio_data['risk_profile']} risk
**Allocation:** {portfolio_data['asset_allocation']['stock']}% stocks, {portfolio_data['asset_allocation']['bond']}% bonds, {portfolio_data['asset_allocation']['crypto']}% crypto
**Performance:** {portfolio_data['metrics']['portfolio_return']:.1f}% return, {portfolio_data['metrics']['sharpe_ratio']:.2f} Sharpe ratio

Provide specific, actionable investment advice. Keep responses under 200 words."""
        
        messages = [{"role": "system", "content": system_prompt}]
        
        if conversation_history:
            messages.extend(conversation_history[-4:])
        
        messages.append({"role": "user", "content": user_message})
        
        return self._make_groq_request(messages, max_tokens=400, stream=True)

def main():
    """Main function for testing the AI advisor"""
    try:
        print("🤖 Initializing QuantAlpha AI Portfolio Advisor...")
        advisor = AIPortfolioAdvisor()
        
        print("\n📊 Running Portfolio Analysis...")
        analysis = advisor.get_portfolio_analysis("comprehensive")
        print(analysis)
        
        print("\n💬 Testing Interactive Chat...")
        response = advisor.chat_with_advisor(
            "What's your assessment of my current crypto allocation? Should I adjust it?"
        )
        print(f"AI Advisor: {response}")
        
        print("\n✅ AI Portfolio Advisor test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n🔧 Setup checklist:")
        print("1. Run: poetry install")
        print("2. Create .env file with: GROQ_API_KEY=your_key")
        print("3. Get API key from: https://console.groq.com")
        print("4. Run: poetry shell")

if __name__ == "__main__":
    main()
