# graph_setup.py
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing import TypedDict, Annotated
from tools_setup import tools  # import tools from tools_setup

from langchain_groq import ChatGroq

def create_graph(groq_api_key: str):
    class State(TypedDict):
        messages: Annotated[list, add_messages]

    llm = ChatGroq(groq_api_key=groq_api_key, model_name="Gemma2-9b-It")
    llm_with_tools = llm.bind_tools(tools=tools)

    def chatbot(state: State):
        return {"messages": [llm_with_tools.invoke(state["messages"])]}

    graph_builder = StateGraph(State)
    graph_builder.add_node("chatbot", chatbot)
    tool_node = ToolNode(tools=tools)
    graph_builder.add_node("tools", tool_node)
    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_conditional_edges("chatbot", tools_condition)
    graph_builder.add_edge("tools", "chatbot")
    graph = graph_builder.compile()
    return graph

