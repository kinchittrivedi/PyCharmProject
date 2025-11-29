from typing_extensions import TypedDict, List
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    values : List[int]
    name : str
    result : str

def process_values(state: AgentState) -> AgentState:
    print(state)

    state["result"] = f"hi there,{state['name']}, your sum is {sum(state['values'])}"

    #print(state)
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

answers = add.invoke({'values': [1,2,3,4], 'name':'kinchit'})
print(answers)
print(answers['result'])



