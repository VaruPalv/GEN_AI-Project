from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import os

from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.tools import tool

# Set your API keys
groq_api_key = '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'
os.environ['TAVILY_API_KEY'] = "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"

# Define available LLMs
MODEL_NAMES = [
    "gemma2-9b-it",
    "llama3-8b-8192",
    "llama3-70b-8192"
]

# Define the calculator tool
@tool
def calculator(expression: str) -> str:
    """Evaluate a math expression and return the result as a string."""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Calculation error: {e}"

# Initialize tools
tool_tavily = TavilySearchResults(max_results=10)
tools = [tool_tavily, calculator]

# FastAPI setup
app = FastAPI(title='Langgraph AI')

# Request model
class RequestState(BaseModel):
    model_name: str
    system_prompt: str
    messages: List[str]

# Chat endpoint
@app.post("/chat")
def chat_endpoint(request: RequestState):
    if request.model_name not in MODEL_NAMES:
        return {"error": "Invalid model name. Please select a valid model."}

    # Set up the LLM and agent
    llm = ChatGroq(groq_api_key=groq_api_key, model_name=request.model_name)
    agent = create_react_agent(llm, tools=tools, state_modifier=request.system_prompt)

    # Prepare initial state
    state = {"messages": request.messages}
    result = agent.invoke(state)

    return result

# Optional: run server manually (only for testing without uvicorn CLI)
# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run(app, host='127.0.0.1', port=8000)
