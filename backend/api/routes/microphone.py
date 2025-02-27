from fastapi import APIRouter, WebSocket, WebSocketDisconnect, FastAPI
import asyncio
from loguru import logger
from openai import OpenAI
import traceback
from backend.api.routes.audio_gateway import audio_gateway
#from backend.gateways.audio_gateway import AudioGateway
from backend.devices.microphone_device import MicrophoneDevice
from dotenv import load_dotenv
import httpx

load_dotenv()

#router = APIRouter()

microphone = MicrophoneDevice("1")
microphone.turn_on()
#audio_gateway = AudioGateway(client=client)

app = FastAPI()

@app.websocket("/microphone_stream")
async def microphone_stream(websocket: WebSocket):
    """Handles WebSocket connections from the microphone."""
    await websocket.accept()
    logger.info("Microphone connected to WebSocket.")
    
    try:
        while True:
            data = await websocket.receive_bytes()
            #logger.info(f"Received {len(data)} bytes of audio data.")
            await asyncio.sleep(0.02)
            #await audio_gateway.send_audio(data)
            async with httpx.AsyncClient(timeout=900.0) as client:
                response = await client.post("http://localhost:8001/send_audio", data=data)
                #logger.debug(f"Sending {len(data)} {type(data)} of audio data.")
                logger.info(f"Response: {response}")
    except WebSocketDisconnect:
        logger.warning("Microphone WebSocket disconnected.")
    except Exception as e:
        logger.error(f"Error streaming audio from microphone: {e}")
        traceback.print_exc()
    finally:
        logger.info("Microphone WebSocket closed.")