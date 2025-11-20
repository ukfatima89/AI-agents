# ai_agent.py
import os
from dotenv import load_dotenv
load_dotenv()
#to remove warnings
os.environ['GRPC_VERBOSITY'] = 'NONE'
os.environ['GLOG_minloglevel'] = '2'

#Step-1: Install required packages
from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch     # NEW package
from langchain_openai import ChatOpenAI 
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage


# #Step-2 Use a current models for the LLM
groq_llm = ChatGroq(model="llama-3.3-70b-versatile")
gemini_llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

#Step-3 Add TavilySearch to tools if API key is available
tools = []
if os.getenv("TAVILY_API_KEY"):
    # TavilySearch is a Tool callable by the agent
    tools = [TavilySearch(max_results=2)]
    
#Step-4 Create the agent with tools and a custom prompt
from langgraph.prebuilt import create_react_agent
from langchain.schema import HumanMessage, AIMessage
system_prompt = "Act as an expert AI chatbot who is smart and friendly"

def get_response_from_ai_agent(llm_id,query, allow_search, system_prompt, provider):
    llm = None
    if provider == "Google":
        llm = ChatGoogleGenerativeAI(model=llm_id)
    elif provider == "Groq":
        llm = ChatGroq(model=llm_id)
    else:
        raise ValueError(f"Unknown LLM provider: {provider}")
    

    tools = [TavilySearch(max_results=2)] if allow_search else []
    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=system_prompt,
    )


    # Step-5 Test run
    
    state = {"messages": [("user", query)]}
    response = agent.invoke(state)
    messages = response.get("messages")
    ai_messages = [message.content for message in messages if isinstance(message, AIMessage ) ]
    return ai_messages[-1]

