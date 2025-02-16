from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
from loguru import logger
from openai import OpenAI
import traceback
from devices.src.gateways.audio_gateway import AudioGateway
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()
router = APIRouter()

audio_gateway = AudioGateway(client=client)

@router.websocket("/microphone_stream")
async def microphone_stream(websocket: WebSocket):
    """Handles WebSocket connections from the microphone."""
    await websocket.accept()
    logger.info("Microphone connected to WebSocket.")
    
    try:
        while True:
            data = await websocket.receive_bytes()
            #logger.info(f"Received {len(data)} bytes of audio data.")
            await asyncio.sleep(0.02)
            await audio_gateway.send_audio(data, client)
    except WebSocketDisconnect:
        logger.warning("Microphone WebSocket disconnected.")
    except Exception as e:
        logger.error(f"Error streaming audio from microphone: {e}")
        traceback.print_exc()
    finally:
        logger.info("Microphone WebSocket closed.")