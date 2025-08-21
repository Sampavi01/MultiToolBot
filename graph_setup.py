# graph_setup.py

"""
This module sets up the LangGraph StateGraph for the multi-agent chatbot.
It integrates the ChatGroq LLM with external tools (like Wikipedia, Arxiv, DuckDuckGo, YouTube, Weather, Python REPL, and Math tools)
and defines the flow between the chatbot node and tool nodes.

Functions:
    create_graph(groq_api_key: str) -> StateGraph
        Creates and compiles a LangGraph StateGraph with ChatGroq and all tools bound.
"""

from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing import TypedDict, Annotated
from tools_setup import tools  # Import all tool instances defined in tools_setup.py

from langchain_groq import ChatGroq


def create_graph(groq_api_key: str):
    """
    Creates and compiles a LangGraph StateGraph with a ChatGroq LLM bound to tools.

    Args:
        groq_api_key (str): The API key for authenticating with the Groq LLM.

    Returns:
        StateGraph: A compiled LangGraph StateGraph ready for streaming/chat usage.

    Notes:
        - The 'State' TypedDict defines the structure of the graph state, here storing a list of chat messages.
        - The 'chatbot' node handles user messages via the LLM.
        - The 'tools' node represents all external tools that the LLM can call.
        - Conditional edges determine when tool calls should be invoked.
    """

    # Define the structure of the chatbot state
    class State(TypedDict):
        # Messages is a list of messages in the conversation, annotated with add_messages
        messages: Annotated[list, add_messages]

    # Initialize ChatGroq LLM with provided API key
    llm = ChatGroq(
        groq_api_key=groq_api_key,
        model_name="Gemma2-9b-It"  # You can switch to other Groq models if desired
    )

    # Bind the LLM to all tools defined in tools_setup.py
    llm_with_tools = llm.bind_tools(tools=tools)

    # Chatbot node function: receives state, invokes LLM with tools, returns updated messages
    def chatbot(state: State):
        """
        Handles user messages by invoking the LLM with the current conversation state.
        """
        return {"messages": [llm_with_tools.invoke(state["messages"])]}

    # Initialize the graph builder with the defined State
    graph_builder = StateGraph(State)

    # Add the main chatbot node to the graph
    graph_builder.add_node("chatbot", chatbot)

    # Add a tool node representing all external tools
    tool_node = ToolNode(tools=tools)
    graph_builder.add_node("tools", tool_node)

    # Connect the start node to the chatbot node
    graph_builder.add_edge(START, "chatbot")

    # Conditional edges determine when the chatbot should call tools
    graph_builder.add_conditional_edges("chatbot", tools_condition)

    # Connect the tool node back to the chatbot to continue conversation after tool calls
    graph_builder.add_edge("tools", "chatbot")

    # Compile the graph for usage in streaming/chat mode
    graph = graph_builder.compile()

    return graph


