from typing import Annotated, Literal
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END, add_messages
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from tools import get_market_data, web_search
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

class State(TypedDict):
    messages: Annotated[list, add_messages]
    next_agent: str 

llm = ChatGroq(model='Llama-3.3-70B-Versatile', temperature=0)
config = {"configurable": {"thread_id": "1"}}
def market_analyst(state: State):
    prompt = "You are a Stock Market Specialist. Use 'get_market_data' to find prices. Return only data."
    messages = [SystemMessage(content=prompt)] + state["messages"]
    response = llm.bind_tools([get_market_data]).invoke(messages)
    return {"messages": [response]}

def news_researcher(state: State):
    prompt = "You are a Financial News Researcher. Use 'web_search' to find recent news. Summarize trends."
    messages = [SystemMessage(content=prompt)] + state["messages"]
    response = llm.bind_tools([web_search]).invoke(messages)
    return {"messages": [response]}

def supervisor(state: State):
    prompt = """
    You are the Manager. Decide who should work next:
    - If you need stock prices, call 'Market_Analyst'.
    - If you need news or events, call 'News_Researcher'.
    - If you have all info to answer the user, call 'FINISH'.
    """
    messages = [SystemMessage(content=prompt)] + state["messages"]
    response = llm.invoke(messages)
    
    content = response.content.upper()
    if "MARKET" in content: return {"next_agent": "Market_Analyst"}
    if "NEWS" in content: return {"next_agent": "News_Researcher"}
    return {"next_agent": "FINISH"}

def create_agent():
    builder = StateGraph(State)
    
    builder.add_node("Supervisor", supervisor)
    builder.add_node("Market_Analyst", market_analyst)
    builder.add_node("News_Researcher", news_researcher)
    
    builder.add_node("market_tools", ToolNode([get_market_data]))
    builder.add_node("news_tools", ToolNode([web_search]))

    builder.add_edge(START, "Supervisor")
    
    builder.add_conditional_edges(
        "Supervisor",
        lambda x: x["next_agent"],
        {
            "Market_Analyst": "Market_Analyst",
            "News_Researcher": "News_Researcher",
            "FINISH": END
        }
    )

    builder.add_edge("Market_Analyst", "market_tools")
    builder.add_edge("market_tools", "Supervisor")
    
    builder.add_edge("News_Researcher", "news_tools")
    builder.add_edge("news_tools", "Supervisor")

    return builder.compile(checkpointer=MemorySaver())