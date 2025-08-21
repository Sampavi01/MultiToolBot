# tools_setup.py

import json
import os
from typing import Optional
from dotenv import load_dotenv

from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper, OpenWeatherMapAPIWrapper
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_core.tools import Tool, tool, BaseTool
from langchain_experimental.utilities import PythonREPL
from youtube_search import YoutubeSearch

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()
OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
if not OPENWEATHERMAP_API_KEY:
    raise ValueError("OPENWEATHERMAP_API_KEY not found in .env file.")

# -----------------------------
# Arxiv Tool
# -----------------------------
arxiv_wrapper = ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=300)
arxiv_tool = ArxivQueryRun(api_wrapper=arxiv_wrapper)

# -----------------------------
# Wikipedia Tool
# -----------------------------
wiki_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=300)
wiki_tool = WikipediaQueryRun(api_wrapper=wiki_wrapper)

# -----------------------------
# DuckDuckGo Search Tool
# -----------------------------
duck_tool = DuckDuckGoSearchRun()

# -----------------------------
# Python REPL Tool
# -----------------------------
python_repl = PythonREPL()
repl_tool = Tool(
    name="python_repl",
    description="Python shell. Input valid Python code and get output dynamically.",
    func=python_repl.run
)

# -----------------------------
# Basic Math Tools
# -----------------------------
@tool
def add(a: float, b: float) -> float:
    """Add two numbers and return the result."""
    return a + b

@tool
def subtract(a: float, b: float) -> float:
    """Subtract second number from first and return the result."""
    return a - b

@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers and return the result."""
    return a * b

@tool
def divide(a: float, b: float) -> float:
    """Divide first number by second. Returns error if divisor is zero."""
    if b == 0:
        return "Error: Division by zero"
    return a / b

# -----------------------------
# YouTube Search Tool
# -----------------------------
class YouTubeSearchTool(BaseTool):
    """
    Search YouTube videos by query.
    
    Input format:
        "query, max_results(optional)"
    """
    name: str = "youtube_search"
    description: str = "Search YouTube. Input: 'query, max_results(optional)'"

    def _search(self, query: str, num_results: int) -> str:
        """
        Perform YouTube search and return a list of video URLs as string.
        """
        results = YoutubeSearch(query, num_results).to_json()
        data = json.loads(results)
        urls = ["https://www.youtube.com" + v["url_suffix"] for v in data["videos"]]
        return str(urls)

    def _run(self, query: str, run_manager: Optional = None) -> str:
        """
        Parse input, handle optional max_results, and call _search.
        """
        parts = query.split(",")
        search_query = parts[0]
        num_results = int(parts[1]) if len(parts) > 1 else 2
        return self._search(search_query, num_results)

youtube_tool = YouTubeSearchTool()

# -----------------------------
# Weather Tool (OpenWeatherMap)
# -----------------------------
weather_tool = Tool(
    name="weather",
    description="Get current weather. Input a city name.",
    func=OpenWeatherMapAPIWrapper(openweathermap_api_key=OPENWEATHERMAP_API_KEY).run
)

# -----------------------------
# Combine all tools into a list for LangGraph
# -----------------------------
tools = [
    wiki_tool,
    arxiv_tool,
    duck_tool,
    repl_tool,
    add, subtract, multiply, divide,
    youtube_tool,
    weather_tool
]


