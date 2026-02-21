import operator
from langchain_core.messages import BaseMessage, HumanMessage
from typing import Annotated, List, TypedDict, Union
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


class TeamState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    next: str   


llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=1.0)






if __name__ == "__main__":
    main()
