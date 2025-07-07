from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.output_parsers import JsonOutputFunctionsParser

def create_supervisor_agent(llm: ChatOpenAI):
    """Creates the supervisor agent for coordinating analysis."""
    
    function_def = {
        "name": "route",
        "description": "Select the next role based on query analysis.",
        "parameters": {
            "title": "routeSchema",
            "type": "object",
            "properties": {
                "next": {
                    "title": "Next",
                    "anyOf": [{"enum": ["Search", "SECAnalyst", "FINISH"]}],
                },
                "reasoning": {
                    "title": "Reasoning",
                    "type": "string",
                    "description": "Explanation for why this agent should act next"
                },
                "information_needed": {
                    "title": "Information Needed",
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of specific information needed from this agent"
                }
            },
            "required": ["next", "reasoning", "information_needed"],
        },
    }

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a financial research team supervisor.
        Your role is to:
        1. Analyze incoming queries
        2. Determine what information is needed
        3. Choose the appropriate agent for each task
        4. Coordinate between agents
        5. Ensure comprehensive analysis"""),
        MessagesPlaceholder(variable_name="messages"),
        ("system", "Who should act next? Consider available information and agent specialties.")
    ])

    return (
        prompt
        | llm.bind_functions(functions=[function_def], function_call="route")
        | JsonOutputFunctionsParser()
    )
