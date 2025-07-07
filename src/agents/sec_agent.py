from langchain.chat_models import ChatOpenAI
from ..tools.analysis import retrieve_information
from ..agents.agent_utils import create_agent

def create_sec_agent(llm: ChatOpenAI):
    """Creates an agent specialized in SEC filings analysis."""
    
    system_prompt = """You are a financial analyst specialized in SEC filings analysis.
    After analyzing SEC filings:
    1. If you need market context, clearly state what specific market data you need
    2. If numbers need industry comparison, explicitly request competitor data
    3. Always include specific numbers and trends from the filings
    4. If you spot significant changes or unusual patterns, highlight them
    
    Format your response as:
    1. Data from SEC Filings: [your findings]
    2. Additional Context Needed: [if any]
    3. Analysis: [your insights]
    """
    
    return create_agent(
        llm=llm,
        tools=[retrieve_information],
        system_prompt=system_prompt
    )
