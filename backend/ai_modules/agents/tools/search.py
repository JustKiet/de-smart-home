from langchain_community.tools import DuckDuckGoSearchRun
from backend.utils.tool_wrapper import tool
from typing import List, Annotated

search_engine = DuckDuckGoSearchRun()

@tool(
    description="Search for information using DuckDuckGo's search engine.",
)
def search(
    query: Annotated[str, "The search query to look up."],
) -> List[str]:
    """Search for information using DuckDuckGo's search engine."""
    return search_engine.invoke(query)
