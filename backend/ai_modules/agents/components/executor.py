from typing import Any, Callable, Dict, List, Optional, Union
import os
from loguru import logger
from openai._types import NOT_GIVEN
from openai import OpenAI
from backend.ai_modules.agents.interfaces.base_executor import BaseExecutor
from backend.ai_modules.agents.components.services.openai_llm_service import OpenAILLMService
from backend.ai_modules.agents.schemas.response import OpenAIResponse
from pydantic import BaseModel
import json


class Executor(BaseExecutor, OpenAILLMService):
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
        OpenAILLMService.__init__(
            self,
            client=client,
            model=model,
            system_message=self.define_system_message(system_message),
            tools=tools,
            api_key=api_key,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
        )
        
    def execute(self, 
                messages: List[Dict[str, str]],
                tools: Optional[List[Dict[str, Any]]] = NOT_GIVEN,
                response_schema: Optional[BaseModel] = NOT_GIVEN,
                **kwargs,
               ) -> Union[OpenAIResponse, BaseModel]:
        kwargs.get("temperature", self._temperature)
        kwargs.get("max_tokens", self._max_tokens)
        kwargs.get("top_p", self._top_p)
        
        if tools == NOT_GIVEN:
            tools = self.tools
        
        context = self.extend_context(messages)
        
        logger.debug(f"Context: {context}")
        
        response = self.model_generate(
            messages=context, 
            tools=tools, 
            response_schema=response_schema
        ).model_dump()
        
        response = {
            "role": "assistant",
            "content": str(response.model_dump()),
        } if response_schema else response
        
        context = self.add_context(response)
        
        logger.info(f"Response Received: {response}" )
        
        if response["tool_calls"] != None and type(response) == dict:
            for tool_call in response.get("tool_calls"):
                tool_call_id = tool_call.get("id")
                tool_name = tool_call.get("function").get("name")
                tool_args = eval(tool_call.get("function").get("arguments"))
                tool_result = self._handle_tool_call(tool_name, **tool_args)
                
                logger.info(f"Tool Result: {tool_result}")
                
                tool_message = {
                    "role": "tool",
                    "tool_call_id": tool_call_id,
                    "content": json.dumps(tool_result),
                }
                
                context = self.add_context(tool_message)
                
            response_with_tool_context = self.model_generate(
                messages=context, 
                tools=tools, 
                response_schema=response_schema
            ).model_dump()
            
            self.add_context(response_with_tool_context)
            
        final_response = self._context_history[-1]
        
        logger.debug(f"Final Response: {final_response}")
        
        if response_schema:
            return response_schema(**final_response)
        
        if response:
            return OpenAIResponse(**final_response)