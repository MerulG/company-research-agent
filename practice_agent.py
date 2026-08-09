from http.client import responses
from pyexpat.errors import messages
from typing import TypedDict, List
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv #store api keys secretly

load_dotenv()

class AgentState(TypedDict):
    messages: list[HumanMessage]

llm = ChatOpenAI(model="gpt-4o")


def process(state:AgentState) -> AgentState:
    responses = llm.invoke(state["messages"])
    print("AI RESPONSE: ",responses.content)
    return state

graph = StateGraph(AgentState)
graph.add_node("process",process)
graph.add_edge(START,"process")
graph.add_edge("process",END)
agent = graph.compile()

user_input = input("Ask something: ")
while user_input!= "exit":
    agent.invoke({"messages":[HumanMessage(user_input)]})
    user_input = input("Ask something: ")