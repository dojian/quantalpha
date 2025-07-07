from langchain.chat_models import ChatOpenAI
from ..tools.search import tavily_search
from ..agents.agent_utils import create_agent

def create_search_agent(llm: ChatOpenAI):
    """Creates a search agent specialized in market research."""
    
    system_prompt = """You are a research assistant who can search for up-to-date 
    financial information using the tavily search engine.
    
    When responding:
    1. Always cite sources
    2. Focus on recent market data and analyst reports
    3. If SEC data is mentioned, compare it with current market views
    4. Highlight any significant discrepancies with official filings
    
    Format your response as:
    1. Market Data: [your findings]
    2. Analyst Views: [key opinions]
    3. Relevance to SEC Data: [if applicable]
    """
    
    return create_agent(
        llm=llm,
        tools=[tavily_search],
        system_prompt=system_prompt
    )
