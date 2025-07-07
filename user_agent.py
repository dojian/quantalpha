import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from uagents_core.crypto import Identity
from fetchai.registration import register_with_agentverse
from fetchai.communication import parse_message_from_agent, send_message_to_agent
from fetchai import fetch
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={r"/api/*": {'origins': 'http://localhost:5174'}})

# Global variables for client identity and responses
primary_agent = None

class PrimaryAgent:
    def __init__(self):
        self.identity = None
        self.latest_response = None
    
    def initialize(self):
        try:
            load_dotenv()
            self.identity = Identity.from_seed(os.getenv("PRIMARY_AGENT_KEY"), 0)
            
            register_with_agentverse(
                identity=self.identity,
                url="http://localhost:5001/webhook",
                agentverse_token=os.getenv("AGENTVERSE_API_KEY"),
                agent_title="Financial Query Router",
                readme="<description>Routes queries to Financial Analysis Agent</description>"
            )
            logger.info("Primary agent initialized successfully!")
                
        except Exception as e:
            logger.error(f"Initialization error: {e}")
            raise

@app.route('/api/search-agents', methods=['GET'])
def search_agents():
    """Search for available agents based on the financial query"""
    try:
        query = request.args.get('query', '')
        if not query:
            return jsonify({"error": "Query parameter 'query' is required."}), 400

        logger.info(f"Searching for agents with query: {query}")
        available_ais = fetch.ai(query)
        agents = available_ais.get('ais', [])
        
        extracted_data = [
            {
                'name': agent.get('name'),
                'address': agent.get('address')
            }
            for agent in agents
        ]
        
        logger.info(f"Found {len(extracted_data)} agents matching the query")
        return jsonify(extracted_data), 200

    except Exception as e:
        logger.error(f"Error finding agents: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/send-request', methods=['POST'])
def send_request():
    try:
        data = request.json
        payload = data.get('payload', {})
        user_input = payload.get('request')
        agent_address = data.get('agentAddress')
        
        if not user_input:
            return jsonify({"error": "No input provided"}), 400
        
        send_message_to_agent(
            primary_agent.identity,
            agent_address,
            {
                "request": user_input
            }
        )
        
        return jsonify({
            "status": "request_sent", 
            "agent_address": agent_address, 
            "payload": payload
        })
        
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/get-response', methods=['GET'])
def get_response():
    try:
        if primary_agent.latest_response:
            response = primary_agent.latest_response
            primary_agent.latest_response = None
            return jsonify(response)
        return jsonify({"status": "waiting"})
    except Exception as e:
        logger.error(f"Error getting response: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_data().decode("utf-8")
        message = parse_message_from_agent(data)
        primary_agent.latest_response = message.payload
        return jsonify({"status": "success"})
    except Exception as e:
        logger.error(f"Error in webhook: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    primary_agent = PrimaryAgent()
    primary_agent.initialize()
    app.run(host="0.0.0.0", port=5001)
