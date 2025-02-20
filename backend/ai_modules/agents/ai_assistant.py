from openai import OpenAI
import os
from typing import Optional, List, Any, Callable, Union, Literal
from backend.ai_modules.agents.schemas.response import OpenAIResponse
from backend.ai_modules.agents.components.context_handler import ContextHandler
from backend.ai_modules.agents.components.executor import Executor
from backend.ai_modules.agents.components.output_handler import OutputHandler
from dotenv import load_dotenv
from openai._types import NOT_GIVEN
from loguru import logger
from pydantic import BaseModel
import base64

load_dotenv()
    
class AIAssistant(ContextHandler,
                  Executor,
                  OutputHandler,):
    def __init__(self, 
                 client: OpenAI,
                 model: str = "gpt-4o-mini",
                 system_message: Optional[str] = None,
                 tools: Optional[List[Callable[..., Any]]] = NOT_GIVEN,
                 api_key: Optional[str] = os.getenv("OPENAI_API_KEY"),
                 temperature: Optional[float] = 0.3,
                 max_tokens: Optional[int] = None,
                 top_p: Optional[float] = None,
                 voice: Optional[Literal["alloy", "ash", "coral", "echo", "fable", "onyx", "nova", "sage", "shimmer"]] = "nova",
                 *args,
                 **kwargs):
        super().__init__(
            client=client,
            model=model,
            system_message=self.define_system_message(system_message),
            tools=tools,
            api_key=api_key,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
        )
        OutputHandler.__init__(
            self,
            client=client,
            voice=voice
        )
        
    def invoke(self, message: str) -> Union[OpenAIResponse, BaseModel]:
        # Check for context
        context = self.get_context(message)
        
        llm_response = self.execute(
            messages=[
                {
                    "role": "user",
                    "content": context,
                }
            ]
        )
        
        speech = self.handle_output(
            output=llm_response.content
        )
        
        llm_response.audio = base64.b64encode(speech).decode("utf-8") if speech else None
        
        return llm_response
    
    
if __name__ == "__main__":
    from backend.ai_modules.agents.tools.search import search
    from backend.ai_modules.agents.tools.get_datetime import get_current_datetime
    from backend.devices.speaker_device import SpeakerDevice
    import pprint
    import time

    
    client = OpenAI()
    
    speaker = SpeakerDevice(device_id="1")
    speaker.turn_on()
    
    assistant = AIAssistant(
        client=client,
        model="gpt-4o-mini",
        tools=[search, get_current_datetime]
    )
    
    start_time = time.time()
    
    response = assistant.invoke(
        message="What's the weather today in Hanoi? Also give me the time and date today."
    )
    
    end_time = time.time()
    
    print(f"Time taken: {end_time - start_time}")
        
    speaker.play_audio(response.audio)
