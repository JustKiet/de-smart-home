from typing import List, Optional, Callable, Any
from loguru import logger
from openai._types import NOT_GIVEN

class ToolLoader:
    def __init__(self,
                 tools: Optional[List[Callable[..., Any]]] = NOT_GIVEN,
                 *args,
                 **kwargs):
        self._tools = [tool.schema for tool in tools] if tools else NOT_GIVEN
        self.tools_map = {
            tool.schema["function"]["name"]: tool for tool in tools
        } if tools is not NOT_GIVEN else NOT_GIVEN
        
    @property
    def tools(self):
        return self._tools
    
    @tools.setter
    def tools(self, tools):
        self._tools = [tool.schema for tool in tools] if tools else NOT_GIVEN
        self.tools_map = {
            tool.schema["function"]["name"]: tool for tool in tools
        } if tools is not NOT_GIVEN else NOT_GIVEN
        return logger.info(f"Binded {len(self._tools)} tools.")
    
    def _handle_tool_call(self, tool_name, **kwargs):
        tool = self.tools_map.get(tool_name)
        if not tool:
            return None
        return tool(**kwargs)
    
    def parse_tool_args(self, response: dict):
        tool_calls = None
        if hasattr(response, "tool_calls") and response.tool_calls is not None:
            tool_calls = [
                {
                    "id": tc.id,
                    "type": tc.type,
                    "function": {
                        "arguments": tc.function.arguments,
                        "name": tc.function.name,
                    },
                }
                for tc in response.tool_calls
            ]
        return tool_calls