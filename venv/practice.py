from typing import TypedDict
import random
from langgraph.graph import StateGraph, START, END
from sympy.codegen import Print
from torchgen.gen_functionalization_type import return_from_mutable_noop_redispatch
from traitlets import This


class AgentState(TypedDict):
    target_number: int
    guess: int
    attempts: int
    lower_bound: int
    upper_bound: int

def setup_node(state:AgentState) -> AgentState:
    """This node sets up the guessing game"""
    state["lower_bound"]=1
    state["upper_bound"]=50
    state["target_number"] = random.randint(1, 50)
    state["guesses"] = []
    state["attempts"] = 0
    print(f"target number is {state['target_number']}")
    return state

def guess_node(state:AgentState) -> AgentState:
    """this generates a guess based on the hint"""
    state["attempts"] = state["attempts"] + 1
    print(f"This is attempt: {state['attempts']}")
    print("Guessing number between ",state["lower_bound"]," and ",state["upper_bound"])
    state["guess"] = random.randint(state["lower_bound"]+1,state["upper_bound"]-1)
    print(f"Guessing: {state['guess']}")
    return state

def hint_node(state:AgentState) -> AgentState:
    """generates a hint based on the last guess"""
    if(state["guess"] < state["target_number"]):
        print("too low...")
        state["lower_bound"] = state["guess"]
    elif(state["guess"] > state["target_number"]):
        print("too high...")
        state["upper_bound"] = state["guess"]
    return state

def should_continue(state:AgentState) -> AgentState:
    """decides if we need to end the stupid game"""
    if(state["guess"] == state["target_number"]):
        print("Number Found! Number: ", state["guess"])
        return "end"
    elif(state["attempts"]>6):
        print("run out of numbers!")
        return "end"
    else:
        return "continue"

graph = StateGraph(AgentState)

graph.add_node("setup",setup_node)
graph.add_node("guess_node",guess_node)
graph.add_node("hint_node",hint_node)

graph.add_edge(START,"setup")
graph.add_edge("setup","guess_node")
graph.add_edge("guess_node","hint_node")

graph.add_conditional_edges(
    "hint_node",
    should_continue,
    {
        "continue":"guess_node",
        "end":END
    }
)

app = graph.compile()

png_bytes = app.get_graph().draw_mermaid_png()
with open("graph.png", "wb") as f:
    f.write(png_bytes)

print(app.invoke({"name":"bob","number":[],"counter":-10}))