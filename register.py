import os
import logging
from flask import Flask, request, jsonify
from uagents_core.crypto import Identity
from fetchai.registration import register_with_agentverse
from fetchai.communication import parse_message_from_agent, send_message_to_agent
from main import init_financial_system
from langchain.schema import HumanMessage
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Global variables
financial_identity = None
research_chain = None

def init_agent():
    """Initialize and register the agent with agentverse"""
    global financial_identity, research_chain
    try:
        # Load environment variables
        load_dotenv()
        
        # Initialize the research chain
        research_chain = init_financial_system()
        
        # Initialize identity and register with Agentverse
        financial_identity = Identity.from_seed("Financial Analysis Agent", 0)
        
        # Register with detailed capabilities description
        register_with_agentverse(
            identity=financial_identity,
            url="http://localhost:5008/webhook",
            agentverse_token=os.getenv("AGENTVERSE_API_KEY"),
            agent_title="Financial Analysis Agent",
            readme = """
                <description>A comprehensive financial analysis agent that combines 
                SEC filing analysis with real-time market data.</description>
                <use_cases>
                    <use_case>Analyze company financial metrics from SEC filings</use_case>
                    <use_case>Research market trends and analyst opinions</use_case>
                    <use_case>Compare financial performance with competitors</use_case>
                </use_cases>
                <payload_requirements>
                    <payload>
                        <requirement>
                            <parameter>query</parameter>
                            <description>What would you like to know about the company's financials?</description>
                        </requirement>
                    </payload>
                </payload_requirements>
            """
        )
        logger.info("Financial Analysis Agent registered successfully!")
    except Exception as e:
        logger.error(f"Error initializing agent: {e}")
        raise

@app.route('/webhook', methods=['POST'])
async def webhook():
    """Handle incoming requests from other agents"""
    try:
        data = request.get_data().decode('utf-8')
        message = parse_message_from_agent(data)
        query = message.payload.get("request", "")
        agent_address = message.sender

        if not query:
            return jsonify({"status": "error", "message": "No query provided"}), 400

        # Process query using research chain
        result = research_chain.invoke({
            "messages": [HumanMessage(content=query)],
            "team_members": ["Search", "SECAnalyst"]
        })

        # Format response
        formatted_result = {
            "analysis": [
                {
                    "role": msg.type if hasattr(msg, 'type') else "message",
                    "content": msg.content,
                    "name": msg.name if hasattr(msg, 'name') else None
                }
                for msg in result.get('messages', [])
            ]
        }

        # Send response back through Agentverse
        send_message_to_agent(
            financial_identity,
            agent_address,
            {'analysis_result': formatted_result}
        )
        return jsonify({"status": "analysis_sent"})

    except Exception as e:
        logger.error(f"Error in webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

def run_agent():
    """Initialize and start the agent"""
    try:
        init_agent()
        app.run(host="0.0.0.0", port=5008, debug=True)
    except Exception as e:
        logger.error(f"Error running agent: {e}")
        raise

if __name__ == "__main__":
    run_agent()
