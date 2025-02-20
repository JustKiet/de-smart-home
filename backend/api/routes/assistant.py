from backend.ai_modules.agents.ai_assistant import AIAssistant
from backend.ai_modules.agents.tools.get_datetime import get_current_datetime
from backend.ai_modules.agents.tools.search import search
from openai import OpenAI
from fastapi import FastAPI, Request
from loguru import logger
from fastapi.exceptions import HTTPException
import json

client = OpenAI()
app = FastAPI()

logger.info("Creating AIAssistant instance.")
assistant = AIAssistant(
    client=client,
    model="gpt-4o-mini",
    tools=[search, get_current_datetime]
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