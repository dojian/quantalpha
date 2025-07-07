import os
import logging
from newsapi import NewsApiClient
from uagents import Agent, Context, Model
from portfolio_manager import PortfolioManager
import json
import aiohttp

# Replace with your NewsAPI key
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_API_URL = os.environ.get("NEWS_API_KEY")

# Setup logging
logging.basicConfig(level=logging.INFO)

# Define message models    
class HelloMessage(Model):
    greeting: str  
    
class WelcomeMessage(Model):
    text: str
    
class FullReport(Model):
    text: str

class UserConfirmation(Model):
    decision: str
    target_allocation: dict
    
# Fetch news function
def fetch_news():
    try:
        newsapi = NewsApiClient(api_key=NEWS_API_KEY)
        result = newsapi.get_top_headlines(language="en", page_size=5)

        if result["status"] != "ok":
            logging.warning(f"NewsAPI returned status: {result['status']}")
            return []

        articles = result.get("articles", [])
        if not articles:
            logging.info("No articles found for the topic.")
            return []

        headlines = []
        for article in articles:
            title = article.get("title", "No title")
            url = article.get("url", "")
            headlines.append(f"{title} ({url})")

        return headlines

    except Exception as e:
        logging.error(f"Error fetching news from NewsAPI: {e}")
        return []

async def analyze_headlines_async(headlines):
    if not headlines:
        return "No headlines to analyze."

    system_prompt = """
        You are a financial advisor.
        Your job is to determine whether the user needs to change 
            his asset allocations based on the context of the discussion. 
        
        If necessary, your recommendations on asset allocations should
            only be in terms of the following segments:
        
            1.  Should he change his allocation among the 
                    following asset classes - Stocks, Bonds, Crypto, and Cash?
            2.  Should he change his allocation among the 
                    following markets - US, Developed, and Emerging Markets?
            3.  Is there any specific news that would cause you to recommend 
                    increasing or reducing his allocation in the current assets he holds?
            
        If you do make any recommendations, be sure to give a 
            rough estimate of the change in allocation.
        
        At the beginning of your answer, only provide the asset class, 
            market, or asset, and the estimate of the allocation change.
        
        Here are some examples:
            
            1.  For asset class: ("Bonds", 10%)
            2.  For market: ("Emerging", -10%)
            3.  For specific asset class: ("AAPL", 5%)
                
        If recommending an asset class or market in which the user does not
            have anything currently allocated, suggest a specific asset they
            might want to include.
            
        Please finish the answer with the new asset class allocations you recommend
            for the portfolio and begin this section with "target allocations".  Only
            show the new allocations for the asset classes.  For example:
            
        target allocations: {stocks:60%, bonds:20%, crypto:10%, cash:10%}            
    """
    pm = PortfolioManager()
        
    user_prompt = (
        "Here are the top headlines for today: " 
        + ", ".join(headlines)
        + "Here are the current asset allocations in my portfolio." 
        + "Asset Type allocation: " 
        + ", ".join([key + " - " + str(value) for key, value in pm.get_asset_allocation().items()])
        + "Region allocation: " 
        + ", ".join([key + " - " + str(value) for key, value in pm.get_geographic_allocation().items()])
        + "Asset allocation: " 
        + ", ".join([asset.symbol + " - " + str(asset.allocation) for asset in pm.portfolio.assets])
        + "Based on this information, which changes should I make to my portfolio?"
    )

    request_payload = {
        "model": "meta-llama/Llama-3.3-70B-Instruct"
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": 500,
        "temperature": 0.3
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(GROQ_API_URL, json=request_payload, headers=headers) as response:
                if response.status == 200:
                    result = await response.json()
                    llama_response = result["choices"][0]["message"]["content"]
                    return llama_response.strip()
                else:
                    print(f"Error: LLaMA API returned status {response.status}")
                    return "Error during LLaMA model inference."
        except Exception as e:
            print(f"Error calling LLaMA API: {e}")
            return "Error during LLaMA model inference."


def parse_analysis(analysis: str):
    allocation = analysis[analysis.index("{")+1:analysis.index("}")].split(",")
    allocation = {
        asset_type.split(":")[0].strip():float(
            asset_type.split(":")[1].replace("%","")
        ) 
        for asset_type in allocation
    }

    return allocation    

# Create the agent
news_agent = Agent(name="news_agent")
news_agent.my_state = {}
client_address = None

@news_agent.on_message(model=HelloMessage)
async def register_client(ctx: Context, sender: str, msg: HelloMessage):
    global client_address
    client_address = sender
    ctx.logger.info(f"Registered new client: {client_address}")
    await ctx.send(client_address, WelcomeMessage(text="You are registered!"))
    
@news_agent.on_interval(period=30)
async def handle_news_request(ctx: Context):
    
    if not client_address:
        ctx.logger.info("Please say hello!")
        return
        
    ctx.logger.info("Checking financial news...")
    headlines = fetch_news()

    if not headlines:
        ctx.logger.warning("No headlines found, sending empty response.")
        return

    ctx.logger.info("Sending headlines to LLaMA for analysis...")
    analysis = await analyze_headlines_async(headlines)
    
    if type(analysis) != str:
        analysis = ""
    
    try:
        target_allocation = parse_analysis(analysis)
    except:
        target_allocation = {}
        
    if not target_allocation:
        ctx.logger.info("LLaMA did not recommend specific allocations.")
        rebalance_question = "\nWould you like to rebalance your portfolio..."
        rebalance_question += "\n1. Based on the minimum variance portfolio?"
        rebalance_question += "\n2. Based on mixed complexity, which factors in rebalancing costs?"
        rebalance_question += "\n3. Do not rebalance."
        rebalance_question += "\nPlease enter the number of your decision"
    else:
        ctx.logger.info("LLaMA recommends specific allocations.")
        rebalance_question = "\nWould you like to rebalance your portfolio..."
        rebalance_question += "\n1. Based on the agent's recommendation?"
        rebalance_question += "\n2. Based on the minimum variance portfolio?"
        rebalance_question += "\n3. Based on mixed complexity, which factors in rebalancing costs?"
        rebalance_question += "\n4. Do not rebalance."
        rebalance_question += "\nPlease enter the number of your decision"

    # Send response with headlines and analysis
    response = "Today's news headlines " + "\n".join(headlines)
    response += "\n"
    
    if analysis != "":
        response += "Analysis " + analysis
        response += "\n"
    
    response += rebalance_question
    ctx.logger.info(response)
    
    full_report = FullReport(text=response)
    decision = await ctx.send(client_address, full_report) 
    await ctx.send(
        client_address, 
        UserConfirmation(decision=decision, target_allocation=target_allocation)
    )

@news_agent.on_message(model=UserConfirmation)
async def handle_user_confirmation(ctx: Context, sender: str, msg: UserConfirmation):
    decision = msg.decision.strip().lower()

    if decision != "4":
        ctx.logger.info("User confirmed rebalancing.")

        # Retrieve stored target allocation
        pm = PortfolioManager()
        
        if decision == "1":
            pm.rebalance_portfolio(msg.target_allocation)
        
        elif decision == "2":
            pm.rebalance_portfolio_mvo()
        
        elif decision == "3":
            pm.rebalance_portfolio_mcp()
            
        portfolio_data = pm.to_dict()    
        print(json.dumps(portfolio_data))
        
        await ctx.send(client_address, "Proceeding with portfolio rebalancing...")        
        
        print("\nPortfolio Summary:")
        print(f"Total Value: ${portfolio_data['total_value']:,.2f}")
        print(f"Number of Assets: {len(portfolio_data['assets'])}")
        print(f"Asset Allocation: {portfolio_data['asset_allocation']}")
        print(f"Geographic Allocation: {portfolio_data['geographic_allocation']}")
        print(f"Portfolio Metrics: {portfolio_data['metrics']}")
        
    else:
        ctx.logger.info("User declined to rebalance.")
        await ctx.send(client_address, "Rebalancing canceled. Let me know if you need anything else.")

if __name__ == "__main__":
    news_agent.run()
