from backend.gateways.audio_gateway import AudioGateway
from openai import OpenAI
from loguru import logger
from fastapi import FastAPI, Request
import traceback

from backend.config import ASSISTANT_SERVER_URL, SPEAKER_SERVER_URL

client = OpenAI()
app = FastAPI()

logger.info("Creating AudioGateway instance.")
audio_gateway = AudioGateway(
    client=client,
    assistant_server_url=ASSISTANT_SERVER_URL,
    speaker_server_url=SPEAKER_SERVER_URL
)

@app.post("/send_audio")
async def send_audio(request: Request):
    """Send audio data to the Speaker WebSocket."""
    audio_data = await request.body()
    #logger.debug(f"Received {len(audio_data)} {type(audio_data)} of audio data.")
    logger.info("Sending audio to Speaker WebSocket...")
    try:
        response = await audio_gateway.send_audio(audio_data)
    except Exception as e:
        logger.error(f"Error sending audio to Speaker WebSocket: {e}")
        traceback.print_exc()
    return {"message": f"Audio sent to Speaker WebSocket. Response: {response}"}