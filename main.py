import operator
from langchain_core.messages import BaseMessage, HumanMessage
from typing import Annotated, List, TypedDict, Union
from langgraph.graph import StateGraph, START, END

class TeamState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    next: str   








if __name__ == "__main__":
    main()
