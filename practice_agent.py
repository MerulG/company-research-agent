from typing import TypedDict, List
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv #store api keys secretly

load_dotenv()

class AgentState(TypedDict):
    messages: list[HumanMessage]

llm = ChatOpenAI(model="gpt-4o")