from typing import TypedDict, List, Union
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv #store api keys secretly

load_dotenv()

class AgentState(TypedDict):
    messages: List[Union[HumanMessage,AIMessage]]

llm = ChatOpenAI(model="gpt-4o")

def process(state:AgentState) -> AgentState:
    """This node processes inputs"""
    response = llm.invoke(state["messages"])

    state["messages"].append(AIMessage(response.content))
    print("AI: ",response.content)
    return state

graph = StateGraph(AgentState)
graph.add_node("process",process)
graph.add_edge(START,"process")
graph.add_edge("process",END)
agent = graph.compile()

conversation_history=[]
user_input = input("Enter: ")
while user_input!= "exit":
    conversation_history.append(HumanMessage(content=user_input))
    if(len(conversation_history) > 6):
        conversation_history.remove(conversation_history[0])
    result = agent.invoke({"messages":conversation_history})

    conversation_history = result["messages"]
    user_input = input("Enter: ")

with open("logging.txt", "w") as file:
    file.write("Your conversation Log:\n")
    for message in conversation_history:
        if isinstance(message,HumanMessage):
            file.write("You: "+message.content+"\n")
        elif isinstance(message,AIMessage):
            file.write("AI: "+message.content+"\n")
    file.write("End of conversation")

print("Conversation saved to logging.txt")