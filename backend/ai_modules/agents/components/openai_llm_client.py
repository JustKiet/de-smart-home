from typing import Any, Callable, Dict, List, Optional, Union
from openai import OpenAI
from openai._types import NOT_GIVEN
from pydantic import BaseModel
from backend.ai_modules.agents.components.tool_loader import ToolLoader
from backend.ai_modules.agents.interfaces.base_llm_model import BaseLLMModel
from backend.ai_modules.agents.schemas.response import OpenAIResponse
import os

class OpenAIClientLLM(BaseLLMModel, ToolLoader):
    def __init__(self, 
                 client: OpenAI,
                 model: str = "gpt-4o-mini",
                 system_message: Optional[str] = None,
                 tools: Optional[List[Callable[..., Any]]] = NOT_GIVEN,
                 api_key: Optional[str] = os.getenv("OPENAI_API_KEY"),
                 temperature: Optional[float] = 0.3,
                 max_tokens: Optional[int] = None,
                 top_p: Optional[float] = None,
                 *args,
                 **kwargs):
        ToolLoader.__init__(
            self,
            tools=tools
        )
        self._client = client
        self._model = model
        self._system_message = self.define_system_message(system_message)
        self._api_key = api_key
        self._temperature = temperature
        self._max_tokens = max_tokens
        self._top_p = top_p
        self._context_history = [
            {
                "role": "system",
                "content": self._system_message,
            }
        ]
        
    def define_system_message(self, message: Optional[str] = None):
        if message is not None:
            self._system_message = message
        default_system_message = """
        You are an home assistant, try to assist the user in everything.\n
        You embrace the persona of JARVIS, Tony Stark's home assistant.\n
        Response in conversational, speech-like manner.\n
        Try to keep it simple and concise.\n
        """
        self._system_message = default_system_message
        return self._system_message
        
    def model_generate(self, 
                       messages: List[Dict[str, str]],
                       tools: Optional[List[Dict[str, Any]]] = None,
                       response_schema: Optional[Any] = NOT_GIVEN) -> Union[OpenAIResponse, BaseModel]:
        if tools is None:
            tools = self.tools
            
        #logger.info(f"Tools: {tools}")

        if response_schema:
            response = (
                self._client.beta.chat.completions.parse(
                    model=self._model,
                    messages=messages,
                    tools=tools,
                    temperature=self._temperature,
                    max_tokens=self._max_tokens,
                    top_p=self._top_p,
                    response_format=response_schema,
                )
                .choices[0]
                .message
            )
            
            if (response.refusal):
                return OpenAIResponse(**response.model_dump())
            else:
                response = response.parsed
        else:
            response = (
                self._client.chat.completions.create(
                    model=self._model,
                    messages=messages,
                    tools=tools,
                    temperature=self._temperature,
                    max_tokens=self._max_tokens,
                    top_p=self._top_p,
                )
                .choices[0]
                .message
            )
            if (response.refusal):
                return OpenAIResponse(**response.model_dump())
            
        # Extract tool_calls arguments
        tool_calls = self.parse_tool_args(response)
            
        if response_schema:
            return response
        
        response = OpenAIResponse(**response.model_dump())
        response.tool_calls = tool_calls
        
        return response
        
    def add_context(self, content: dict):
        self._context_history.append(content)
        return self._context_history
        
    def extend_context(self, content: List[dict[str, str]]):
        self._context_history.extend(content)
        return self._context_history
    
    #def eval_response(self, response: str):
    #    if type(response) == str:
    #        return ast.literal_eval(response)
    #    else:
    #        return response