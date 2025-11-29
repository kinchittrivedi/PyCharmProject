from typing_extensions import TypedDict, List
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    name: str
    age: str
    skill: str
    final: str

def first_node(state:AgentState) -> AgentState:
    """This is the first node of our sequence"""

    state["final"] = f"Hi {state["name"]}!"
    return state

def second_node(state:AgentState) -> AgentState:
    """This is the second node of our sequence"""

    state["final"] = state["final"] + f" You are {state["age"]} years old!"

    return state

def third_node(state:AgentState) -> AgentState:
    """This is the third node of our sequence"""
    state["final"] = state["final"] + f" you have skills in {state["skill"]}"

    return state

graph = StateGraph(AgentState)
graph.add_node("first_node", first_node)
graph.add_node("second_node", second_node)
graph.add_node("third_node",third_node)

graph.set_entry_point("first_node")
graph.add_edge("first_node", "second_node")
graph.add_edge("second_node","third_node")
graph.set_finish_point("third_node")
add = graph.compile()

from IPython.display import Image, display
image_data = add.get_graph().draw_mermaid_png()

with open("excercise3.png", "wb") as f:
    f.write(image_data)

answers = add.invoke({'age': 15, 'name':'kinchit', 'skill':'python and genAI'})
print(answers)




