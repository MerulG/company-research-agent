from typing import TypedDict, Annotated, Sequence
#sequence automatically handles chat history by adding messages
#annotated provides additional context via metadata without affecting the type itself
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.messages import SystemMessage
from langchain_core.messages import ToolMessage
from langchain_core.messages import BaseMessage
from langchain_core.tools import tool
from langgraph.graph.message import add_messages #reducer function - preserves state by appending rather than overriding
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from dotenv import load_dotenv #store api keys secretly

load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage],add_messages] #the add_messages here will append rather than overwrite

@tool
def add(a:int,b:int):
    """This is an addition function that adds two numbers together"""
    return a+b

@tool
def subtract(a:int,b:int):
    """This is a subtraction function that subtracts two numbers"""
    return a-b

@tool
def multiply(a:int,b:int):
    """This is a multiplication function that multiples two numbers together"""
    return a*b

tools = [add,subtract,multiply]

model = ChatOpenAI(model="gpt-4o").bind_tools(tools)

def model_call(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(content=
        "You are my AI assistant, please answer my query to the best of your ability"
    )
    #invoke the model with teh system prompt, human query then update the state
    response = model.invoke([system_prompt] + state["messages"])
    return {"messages":[response]} #This is a compact way of updating the state -> the messages will be appended by the response

def should_continue(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]
    if not last_message.tool_calls:
        return "end"
    else:
        return "continue"

graph = StateGraph(AgentState)
graph.add_node("our_agent",model_call)

tool_node = ToolNode(tools=tools)
graph.add_node("tools",tool_node)

graph.add_edge(START,"our_agent")

graph.add_conditional_edges(
    "our_agent",
    should_continue,
    {
        "continue":"tools",
        "end":END
    }
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

inputs={"messages":[("user","add 34 + 21. Add 3 + 7. multiply 34 and 5. subtract 4 and 6")]}
print_stream(app.stream(inputs,stream_mode="values"))









