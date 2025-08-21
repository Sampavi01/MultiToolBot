# app.py
import os
import streamlit as st
from dotenv import load_dotenv
from graph_setup import create_graph

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file.")
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

# -----------------------------
# Create LangGraph
# -----------------------------
graph = create_graph(groq_api_key=GROQ_API_KEY)

# -----------------------------
# Streamlit page config & header
# -----------------------------
st.set_page_config(
    page_title="✨ QueryMaster",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <h1 style='text-align: center; color: #FFD700;'>✨ QueryMaster</h1>
    <h3 style='text-align: center; color: #FFA500;'>Your AI multi-tool assistant</h3>
    <hr style='border:1px solid #444444'>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Sidebar: Tools description
# -----------------------------
st.sidebar.title("🛠️ Available Tools")
st.sidebar.markdown("""
- **Math Calculations:** Perform basic arithmetic operations.  
- **Wikipedia & Arxiv:** Retrieve summaries, articles, and research papers.  
- **DuckDuckGo Search:** Search the web for general information.  
- **YouTube:** Find relevant videos on any topic or person.  
- **Weather:** Get current weather information for any city.  
- **Python REPL:** Execute Python code dynamically.  

All tools are integrated — just type your query naturally, and QueryMaster will decide which tool to use.
""")
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/4712/4712170.png", width=120)

# -----------------------------
# Dark-mode background
# -----------------------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0D1117;
        color: #C9D1D9;
    }
    .stSidebar {
        background-color: #161B22;
        color: #C9D1D9;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Initialize chat messages
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Function for styled chat bubble (dark mode)
# -----------------------------
def chat_bubble(message, role="user"):
    if role == "user":
        color_bg = "#1F2937"  # dark gray
        color_border = "#6366F1"  # indigo
        text_color = "#E0E7FF"
    else:
        color_bg = "#111827"  # almost black
        color_border = "#10B981"  # green
        text_color = "#A7F3D0"

    return f"""
    <div style="
        background: {color_bg};
        color: {text_color};
        padding: 12px; 
        border-radius: 12px;
        border: 1px solid {color_border};
        max-width: 80%;
        margin-bottom: 8px;
        ">
        {message}
    </div>
    """

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(chat_bubble(message["content"], message["role"]), unsafe_allow_html=True)

# -----------------------------
# Chat input
# -----------------------------
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(chat_bubble(prompt, "user"), unsafe_allow_html=True)

    graph_input = {"messages": [("user", prompt)]}

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        with st.spinner("QueryMaster is thinking..."):
            events = graph.stream(graph_input, stream_mode="values")
            for event in events:
                last_message = event["messages"][-1]
                if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
                    tool_call_info = f"Calling tool: `{last_message.tool_calls[0]['name']}` with args: `{last_message.tool_calls[0]['args']}`"
                    message_placeholder.markdown(f"🛠️ {tool_call_info}")
                else:
                    full_response = last_message.content
                    message_placeholder.markdown(chat_bubble(full_response, "assistant"), unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": full_response})



