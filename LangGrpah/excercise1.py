from typing import Dict
from typing_extensions import TypedDict

from langgraph.graph import StateGraph

# We now create an AgentState - shared data structure that keeps track of information as your application runs.

class AgentState(TypedDict): # Our state schema
    name : str


def compliment_node(state: AgentState) -> AgentState:
    """Simple node that compliments the user"""

    state['name'] = state["name"] + " you're doing an amazing job learning LangGraph!"

    return state

graph = StateGraph(AgentState)

graph.add_node("compliment", compliment_node)

graph.set_entry_point("compliment")
graph.set_finish_point("compliment")

app = graph.compile()

from IPython.display import Image, display
image_data = app.get_graph().draw_mermaid_png()

with open("excercise1.png", "wb") as f:
    f.write(image_data)

print("✅ Graph saved as graph.png")

result = app.invoke({"name": "Bob"})
print(result["name"])
