from backend.ai_modules.agents.ai_assistant import AIAssistant
from backend.ai_modules.agents.tools.get_weather import get_weather
from backend.ai_modules.agents.tools.search import search
from openai import OpenAI
from fastapi import FastAPI, Request
from loguru import logger
from fastapi.exceptions import HTTPException

from backend.ai_modules.agents.components.executor import Executor
from backend.ai_modules.agents.components.handlers.output_handler import OutputHandler
from backend.ai_modules.agents.components.handlers.context_handler import ContextHandler
from backend.ai_modules.agents.components.services.lightning_speech_service import LightningSpeechService

import json

client = OpenAI()
app = FastAPI()

logger.info("Creating AIAssistant instance.")

speech_client = LightningSpeechService()

context_handler = ContextHandler()

executor = Executor(
    client=client,
    tools=[search, get_weather]
)

output_handler = OutputHandler(
    speech_client=speech_client
)

assistant = AIAssistant(
    context_handler=context_handler,
    executor=executor,
    output_handler=output_handler
)

@app.post("/invoke_assistant")
async def invoke(message: Request):
    """Invoke the AI Assistant with a message."""
    body = await message.body()
    if not body:
        raise HTTPException(status_code=400, detail="Empty request body")
    
    try:
        message_data = await message.json()
        message_data = message_data["message"]
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    logger.info(f"Message: {message_data}")
    logger.info(f"Message type: {type(message_data)}")
    logger.info(f"Invoking AI Assistant with message: {message_data}")
    response = assistant.invoke(message=message_data)
    return response