import pyaudio
import asyncio
import threading
from fastapi import FastAPI, WebSocket
from devices.src.smart_devices.interfaces.control_microphone import ControlMicrophone
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import traceback
from starlette.websockets import WebSocketDisconnect
class MicrophoneDevice(ControlMicrophone):
    def __init__(self, device_id: str, gateway_url: str):
        super().__init__()
        self._state = 'off'
        self._muted = False
        self.device_id = f"microphone_{device_id}"
        self._pyaudio = pyaudio.PyAudio()
        self.gateway_url = gateway_url
        self._streaming = False
        self._thread = None
        self._format = pyaudio.paInt16
        self._channels = 1
        self._rate = 16000
        self._chunk_size = 4096
        
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self._format,
            channels=self._channels,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk_size
        )
        
    def is_turned_on(self):
        """Check if the microphone is turned on."""
        if self._state == 'on':
            return True
        else:
            raise Exception(f"{self.device_id} | Microphone is turned off. Please turn the device on first.")
    
    def turn_on(self):
        """Turn on the microphone."""
        self._state = 'on'
        logger.info(f"{self.device_id} | Microphone turned on.")
        return self.get_status()
    
    def turn_off(self):
        """Turn off the microphone."""
        self._state = 'off'
        logger.info(f"{self.device_id} | Microphone turned off.")
        return self.get_status()
    
    def mute(self):
        """Mute the microphone."""
        self.is_turned_on()
        
        self._muted = True
        logger.info(f"{self.device_id} | Microphone muted.")
        return self.get_status()
    
    def unmute(self):
        """Unmute the microphone."""
        self.is_turned_on()
        
        self._muted = False
        logger.info(f"{self.device_id} | Microphone unmuted.")
        return self.get_status()
    
    async def capture_audio(self, websocket: WebSocket):
        if not self.is_turned_on():
            await websocket.close()
            return
        
        await websocket.accept()
        stream = self._pyaudio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
        
        try:
            while self._state == 'on':
                if not self._muted:
                    data = stream.read(1024, exception_on_overflow=False)
                    try:
                        logger.info(f"{self.device_id} | Sending {len(data)} bytes of audio data.")
                        await websocket.send_bytes(data)
                    except WebSocketDisconnect:
                        logger.warning(f"{self.device_id} | WebSocket client disconnected. Stopping audio stream.")
                        break
        except Exception as e:
            logger.error(f"{self.device_id} | Error capturing audio: {e}")
            logger.error(f"{self.device_id} | {traceback.format_exc()}")
        finally:
            stream.stop_stream()
            stream.close()
            
    async def stream_audio(self):
        """Continuously record and yield audio data as bytes."""
        self.is_turned_on()

        self._streaming = True
        try:
            while self._streaming and self._state == 'on':
                audio_chunk = await asyncio.to_thread(self.stream.read, self._chunk_size, exception_on_overflow=False)
                yield audio_chunk  # ✅ Yield raw PCM audio
                await asyncio.sleep(0.02)  # Simulate processing delay

        except Exception as e:
            logger.error(f"{self.device_id} | Error recording audio: {e}")
        finally:
            self.stream.stop_stream()
            self.stream.close()
            self.p.terminate()
            self._streaming = False
            
    def pause_audio(self):
        """Pause the audio stream."""
        self.is_turned_on()
        self._pause_event.clear()
        logger.error(f"{self.device_id} | Audio stream paused.")
        return self.get_status()
    
    def resume_audio(self):
        """Resume the audio stream."""
        self.is_turned_on()
        self._pause_event.set()
        logger.error(f"{self.device_id} | Audio stream resumed.")
        return self.get_status()
    
    def get_status(self):
        """Get device status."""
        self.is_turned_on()
        
        return {
            'device_id': self.device_id,
            'state': self._state,
            'muted': self._muted,
            'streaming': self._streaming,
            'format': self._format,
            'streaming': self._streaming,
            'channels': self._channels,
            'rate': self._rate,
            'chunk_size': self._chunk_size,
            'gateway_url': self.gateway_url
        }