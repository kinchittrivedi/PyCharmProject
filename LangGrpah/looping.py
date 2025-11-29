from typing_extensions import TypedDict, List
from langgraph.graph import StateGraph, START, END
import random


class AgentState(TypedDict):
    name: str
    number: List[int]
    counter: int

def greeting_node(state: AgentState) -> AgentState:
    """Greeting Node which says hi to the person"""
    state["name"] = f"Hi there, {state["name"]}"
    state["counter"] = 0

    return state

def random_node(state: AgentState) -> AgentState:
    """Generates a random number from 0 to 10"""
    state["number"].append(random.randint(0, 10))
    state["counter"] += 1

    return state


def should_continue(state: AgentState) -> AgentState:
    """Function to decide what to do next"""
    if state["counter"] < 5:
        print("ENTERING LOOP", state["counter"])
        return "loop"  # Continue looping
    else:
        return "exit"  # Exit the loop

graph = StateGraph(AgentState)

graph.add_node("greeting", greeting_node)
graph.add_node("random", random_node)
graph.add_edge("greeting", "random")


graph.add_conditional_edges(
    "random",     # Source node
    should_continue, # Action
    {
        "loop": "random",
        "exit": END
    }
)

graph.set_entry_point("greeting")

add = graph.compile()

from IPython.display import Image, display
image_data = add.get_graph().draw_mermaid_png()

with open("looping.png", "wb") as f:
    f.write(image_data)

#add.invoke({"name":"Vaibhav", "number":[], "counter":-1})
initial_state_1 = AgentState(name="Vaibhav", number=[], counter=-1)
print(add.invoke(initial_state_1))

