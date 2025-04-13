from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict
from typing import Annotated



class State(TypedDict):
    messages: Annotated[list, add_messages]

__all__ = ['State']