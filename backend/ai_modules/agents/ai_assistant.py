from openai import OpenAI
import os
from typing import Optional, List, Any, Callable, Union, Literal
from backend.ai_modules.agents.schemas.response import OpenAIResponse
from backend.ai_modules.agents.components.handlers.context_handler import ContextHandler
from backend.ai_modules.agents.components.executor import Executor
from backend.ai_modules.agents.components.handlers.output_handler import OutputHandler

from backend.ai_modules.agents.interfaces.base_executor import BaseExecutor

from dotenv import load_dotenv
from openai._types import NOT_GIVEN
from loguru import logger
from pydantic import BaseModel
import base64

load_dotenv()
    
class AIAssistant:
    def __init__(self,
                 context_handler: ContextHandler,
                 executor: BaseExecutor,
                 output_handler: OutputHandler
                ):
        self.context_handler = context_handler
        self.executor = executor
        self.output_handler = output_handler
        
    def invoke(self, message: str) -> Union[OpenAIResponse, BaseModel]:
        # Check for context
        context = self.context_handler.get_context(message)
        
        llm_response = self.executor.execute(
            messages=[
                {
                    "role": "user",
                    "content": context,
                }
            ]
        )
        
        speech = self.output_handler.handle_output(
            output=llm_response.content
        )
        
        llm_response.audio = speech
        llm_response.audio = base64.b64encode(speech).decode("utf-8") if speech else None
        
        return llm_response    
    
if __name__ == "__main__":
    from backend.ai_modules.agents.tools.search import search
    from backend.ai_modules.agents.tools.get_weather import get_weather
    from backend.devices.speaker_device import SpeakerDevice
    from backend.ai_modules.agents.components.services.openai_speech_service import OpenAISpeechService
    from backend.ai_modules.agents.components.services.lightning_speech_service import LightningSpeechService
    import pprint
    import time
    
    client = OpenAI()
    speech_client = LightningSpeechService()
    
    speaker = SpeakerDevice(device_id="1")
    speaker.turn_on()
    
    context_handler = ContextHandler()
    
    executor = Executor(
        client=client,
        tools=[search, get_weather]
    )
    
    output_handler = OutputHandler(speech_client=speech_client)
    
    assistant = AIAssistant(
        context_handler=context_handler,
        executor=executor,
        output_handler=output_handler
    )
    
    start_time = time.time()
    
    response = assistant.invoke(
        message="Forecast the next few days weather for me please. Also give me the time and date today."
    )
    
    end_time = time.time()
    
    print(f"Time taken: {end_time - start_time}")
        
    speaker.play_audio(response.audio)


