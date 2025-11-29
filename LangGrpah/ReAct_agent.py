from typing_extensions import Annotated, Sequence, TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage # The foundational class for all message types in LangGraph
from langchain_core.messages import ToolMessage # Passes data back to LLM after it calls a tool such as the content and the tool_call_id
from langchain_core.messages import SystemMessage # Message for providing instructions to the LLM
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
import perplexity
import os

load_dotenv()

class Agentstate(TypedDict):
    messages: Annotated[Sequence[BaseMessage],add_messages]

@tool
def add(a:int,b:int):
    """This is an addition function that adds 2 numbers together"""
    return a+b

@tool
def subtract(a:int,b:int):
    """This is an subtraction function that adds 2 numbers together"""
    return a - b

@tool
def multiply(a:int,b:int):
    """This is an multiplication function that adds 2 numbers together"""
    return a * b

tools = [add,subtract,multiply]

llm = ChatOpenAI(
    model="sonar",  # or "sonar", "sonar-medium", etc.
    openai_api_key=os.getenv("PERPLEXITY_API_KEY"),
    openai_api_base="https://api.perplexity.ai",  # 👈 key difference!
).bind_tools(tools) #this will not work as perplexity is not providing binding tools functionalities

def model_call(state:Agentstate) -> Agentstate:
    system_prompt = SystemMessage(content = " You are my AI assistant, please answer my query to the best of your ability.")
    response = llm.invoke([system_prompt]+state["messages"])
    return {"messages":[response]}

def should_continue(state:Agentstate):
    messages = state["messages"]
    last_message = messages[-1]
    if not last_message.tool_calls:
        return "end"
    else:
        return "continue"

graph = StateGraph(Agentstate)
graph.add_node("our_agent",model_call)

tool_node = ToolNode(tools=tools)
graph.add_node("tools",tool_node)

graph.set_entry_point("our_agent")

graph.add_conditional_edges(
    "our_agent",
    should_continue,
    {
                "continue":"tools",
                "end":END,
            },
)

graph.add_edge("tools","our_agent")

app = graph.compile()

def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message,tuple):
            print(message)
        else:
            message.pretty_print()
inputs = {"messages": [("user","add 40+60 and then multiply is by 9 and substract 200 from it. Tell me what is the capital of India")]}
print_stream(app.stream(inputs,stream_mode="values"))
