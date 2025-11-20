#Step-1: Setup pydantic models(Schema Validation)
    #frisr install pydantic
from pydantic import BaseModel
from typing import List

class RequestState(BaseModel):
    model_name: str
    model_provider: str
    system_prompt: str
    messages: List[str]
    allow_search: bool



#Step-2: Setup AI Agent from frontend request
#install fastapi
from fastapi import FastAPI
from ai_agent import get_response_from_ai_agent

ALLOWED_MODEL_NAMES = ["gemini-2.5-flash", "llama-3.3-70b-versatile"]

app = FastAPI(title = "Chatbot AI Agent")

@app.post("/chat")
def chat_endpoint(request: RequestState):
    """API endpoint to interact with the AI agent using langgraph and search tools.
       It dynamically selects the model specified in the request
    """
    if request.model_name not in ALLOWED_MODEL_NAMES:
        return {"error": "Model not allowed. Please choose a valid ai model."}
    
    llm_id=request.model_name
    query=request.messages[-1]
    allow_search=request.allow_search
    system_prompt=request.system_prompt
    provider=request.model_provider

    #Create AI Agent and get response from it.
    response = get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider)
    return {"response": response}

#Step-3: Run app & explore swagger UI docs
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host ="127.0.0.1", port = 9999)