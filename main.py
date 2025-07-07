import os
import logging
from dotenv import load_dotenv
from src.rag.chain import create_rag_chain
from src.graph.state import create_research_graph
from langchain.schema import HumanMessage

logger = logging.getLogger(__name__)

def init_financial_system():
    """Initialize the RAG and research system."""
    try:
        # Create RAG chain for SEC document analysis
        rag_chain = create_rag_chain("data/raw/apple_10k.pdf")
        
        # Initialize research graph with RAG chain
        chain = create_research_graph(rag_chain)
        
        return chain
    except Exception as e:
        logger.error(f"Error initializing system: {e}")
        raise

async def run_financial_analysis(query: str):
    """
    Process financial analysis queries through the research graph.
    
    Args:
        query (str): The financial analysis query to process
    
    Returns:
        dict: Analysis results from multiple agents
    """
    try:
        # Initialize state with query
        state = {
            "messages": [HumanMessage(content=query)],
            "team_members": ["Search", "SECAnalyst"],
            "information_needed": [],
            "reasoning": ""
        }
        
        # Process through research chain
        result = research_chain.invoke(state)
        
        return {
            "status": "success",
            "analysis": result.get("messages", [])
        }
        
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        return {
            "status": "error",
            "message": str(e)
        }

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    # Initialize the system
    research_chain = init_financial_system()
