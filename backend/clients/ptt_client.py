import asyncio
import websockets
import keyboard
from loguru import logger
from backend.api.routes.microphone import microphone

from backend.config import MICROPHONE_SERVER_URL

async def press_to_talk_client():
    try:
        logger.info(MICROPHONE_SERVER_URL)
        async with websockets.connect(MICROPHONE_SERVER_URL) as websocket:
            logger.info("Connected to WebSocket Server at:", MICROPHONE_SERVER_URL)
            
            while True:
                input("Press Enter to start recording...")
                logger.info("Recording started, press 'q' to stop.")
                frames = []
                while True:
                    audio_data = microphone.stream.read(microphone._chunk_size)
                    frames.append(audio_data)
                    if keyboard.is_pressed("q"):
                        break
                logger.info("Recording stopped. Sending audio...")
                
                await websocket.send(b"".join(frames))
                data = await websocket.recv()
                
                logger.info(f"Received: {data}")
                logger.info("Audio sent to WebSocket Server")
    except websockets.exceptions.ConnectionClosed:
        logger.warning("Connection closed by server")
    finally:
        logger.info("Closing WebSocket client connection")
        
if __name__ == "__main__":
    try:
        asyncio.run(press_to_talk_client())
    except KeyboardInterrupt:
        print("\nStreaming stopped by user. Exiting gracefully.")