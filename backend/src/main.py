import asyncio
import websockets
from fastapi import FastAPI, WebSocket
from devices.src.smart_devices.microphone_device import MicrophoneDevice
from devices.src.smart_devices.speaker_device import SpeakerDevice
from devices.src.gateways.audio_gateway import AudioGateway
from fastapi.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocketDisconnect
from loguru import logger
import traceback
from openai import OpenAI
from dotenv import load_dotenv
import keyboard
import uvicorn

from backend.src.api.routes import microphone, speaker

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change for security)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI()

audio_gateway = AudioGateway(client)

audio_gateway.add_microphone("1")
audio_gateway.add_speaker("1")

app.include_router(microphone.router, prefix="/microphone", tags=["Microphone"])
app.include_router(speaker.router, prefix="/speaker", tags=["Speaker"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)