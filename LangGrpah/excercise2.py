from typing_extensions import TypedDict, List
from langgraph.graph import StateGraph
import math

class AgentState(TypedDict):
    values : List[int]
    operation : str
    name : str
    result : str

def process_values(state: AgentState) -> AgentState:
    """This function handles multiple different inputs"""
    if state["operation"] == "+":
        state["result"] = f"Hi {state['name']}, your answer is: {sum(state['values'])}"
    elif state["operation"] == "*":
        state["result"] = f"Hi {state['name']}, your answer is: {math.prod(state['values'])}"
    else:
        state["result"] = "Invalid!"

    return state

graph = StateGraph(AgentState)
graph.add_node("processor", process_values)
graph.set_entry_point("processor")
graph.set_finish_point("processor")
add = graph.compile()

from IPython.display import Image, display
image_data = add.get_graph().draw_mermaid_png()

with open("multiple_inputs.png", "wb") as f:
    f.write(image_data)

answers = add.invoke({'values': [1,2,3,4], 'name':'kinchit', 'operation':'*'})
print(answers)
print(answers['result'])



