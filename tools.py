from datetime import datetime

from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

_search = DuckDuckGoSearchRun()
_wiki = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=10000)
)


@tool
def search_tool(query: str) -> str:
    """Search the web for current information."""
    try:
        return _search.invoke(query) or "No results found."
    except Exception as e:
        # crash ki jagah error text return, taaki agent aage badh sake
        return f"Web search failed: {e}"


@tool
def wiki_tool(query: str) -> str:
    """Look up factual background information on Wikipedia."""
    try:
        return _wiki.invoke(query) or "No results found."
    except Exception as e:
        return f"Wikipedia lookup failed: {e}"


def save_to_txt(data: str, filename: str = "research_output.txt") -> str:
    """Append research output to a text file with a timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(text)

    return f"Data successfully saved to {filename}"