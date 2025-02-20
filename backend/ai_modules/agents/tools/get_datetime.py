import datetime
from backend.utils.tool_wrapper import tool
from typing import List, Annotated

@tool(
    description="Get the current date and time."
)
def get_current_datetime() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")