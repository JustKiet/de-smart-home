import pyaudio
import asyncio
import threading
from fastapi import FastAPI, WebSocket
from devices.src.smart_devices.interfaces.control_microphone import ControlMicrophone
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import traceback
from starlette.websockets import WebSocketDisconnect
import webrtcvad


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
    
    def turn_on(self):
        """Turn on the microphone."""
        self._state = 'on'
        return self.get_status()
    
    def turn_off(self):
        """Turn off the microphone."""
        self._state = 'off'
        return self.get_status()
    
    def mute(self):
        """Mute the microphone."""
        self._muted = True
        return self.get_status()
    
    def unmute(self):
        """Unmute the microphone."""
        self._muted = False
        return self.get_status()
    
    async def capture_audio(self, websocket: WebSocket):
        if self._state == 'off':
            await websocket.close()
            return
        
        await websocket.accept()
        stream = self._pyaudio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
        
        try:
            while self._state == 'on':
                if not self._muted:
                    data = stream.read(1024, exception_on_overflow=False)
                    try:
                        logger.info(f"Sending {len(data)} bytes of audio data.")
                        await websocket.send_bytes(data)
                    except WebSocketDisconnect:
                        logger.warning("WebSocket client disconnected. Stopping audio stream.")
                        break
        except Exception as e:
            logger.error(f"Error capturing audio: {e}")
            logger.error(traceback.format_exc())
        finally:
            stream.stop_stream()
            stream.close()
            
    async def record_audio(self):
        """Continuously record and yield audio data as bytes."""
        if self._state != 'on':
            raise RuntimeError("Microphone is off. Turn it on before recording.")

        self._streaming = True
        try:
            while self._streaming and self._state == 'on':
                audio_chunk = await asyncio.to_thread(self.stream.read, self._chunk_size, exception_on_overflow=False)
                yield audio_chunk  # ✅ Yield raw PCM audio
                await asyncio.sleep(0.02)  # Simulate processing delay

        except Exception as e:
            print(f"❌ Error recording audio: {e}")
        finally:
            self.stream.stop_stream()
            self.stream.close()
            self.p.terminate()
            self._streaming = False
            
    def pause_audio(self):
        """Pause the audio stream."""
        self._pause_event.clear()
        return self.get_status()
    
    def resume_audio(self):
        """Resume the audio stream."""
        self._pause_event.set()
        return self.get_status()
    
    def get_status(self):
        return {
            'device_id': self.device_id,
            'state': self._state,
            'muted': self._muted,
        }