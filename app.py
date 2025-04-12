from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from langchain_community.tools.tavily_search import TavilySearchResults
import os
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
import uvicorn

groq_api_key='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'
os.environ['TAVILY_API_KEY']="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"

MODEL_NAMES= [
    "llama-guard-3-8b",
    "gemma2-9b-it",
    "mixtral-8x7b-32768",
    "llama3-8b-8192",
    "llama3-70b-8192"
]
tool_tavily= TavilySearchResults(max_results=10)

tools=[tool_tavily, ]
app= FastAPI(title='Langgraph AI')

class RequestState(BaseModel):
    model_name: str
    system_prompt: str
    messages: List[str]

@app.post("/chat")
def chat_endpoint(request:RequestState):
    if request.model_name not in MODEL_NAMES:
        return {"error":"Invalid model name. Please select a valid Model."}
    llm=ChatGroq(groq_api_key=groq_api_key, model_name=request.model_name)
    agent= create_react_agent(llm,tools=tools, state_modifier=request.system_prompt)

    state={"messages":request.messages}
    result =agent.invoke(state)

    return result

# if __name__=='__main__':
#     import uvicorn
#     uvicorn.run(app,host='127.0.0.1',port=8000)



