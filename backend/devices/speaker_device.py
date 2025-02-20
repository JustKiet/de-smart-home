from backend.devices.interfaces.control_speaker import ControlSpeaker
import pyaudio
import threading
from typing import Literal, Optional
import sounddevice as sd
import numpy as np
from loguru import logger
import io
import soundfile as sf
import scipy.signal as sps

class SpeakerDevice(ControlSpeaker):
    def __init__(self, device_id: str):
        super().__init__()
        self._state = 'off'
        self._volume = 1.0
        self._muted = False
        self._device_id = f"speaker_{device_id}"
        self._audio_status: Literal['playing', 'paused', 'stopped'] = 'stopped'
        self._pause_event = threading.Event()
        self._pause_event.set()
        self._thread = None
        self._streaming = False
        
        self._chunk_size = 4096
        self.sample_rate = 16000
        self._channels = 1
        self._format = pyaudio.paInt16
        
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self._format,
            channels=self._channels,
            rate=self.sample_rate,
            output=True,
            frames_per_buffer=self._chunk_size
        )
        
    @property
    def device_id(self):
        return self._device_id
        
    def is_turned_on(self):
        if self._state == 'on':
            return True
        else:
            raise Exception(f"{self._device_id} | Speaker is turned off. Please turn the device on first.")
        
    def turn_on(self):
        self._state = 'on'
        return self.get_status(attribute='state')
        
    def turn_off(self):
        self._state = 'off'
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        return self.get_status(attribute='state')
    
    def set_volume(self, value: int):
        self.is_turned_on()
        self._volume = value
        return self.get_status(attribute='volume')
    
    def mute(self):
        self.is_turned_on()
        self._muted = True
        return self.get_status(attribute='muted')
    
    def unmute(self):
        self.is_turned_on()
        self._muted = False
        return self.get_status(attribute='muted')
    
    def resample_audio(self, wav_bytes, target_sr=16000):
        """
        Resamples WAV audio from any sample rate to `target_sr` (default: 16 kHz).
        
        Parameters:
            wav_bytes (bytes): Input WAV audio data as bytes.
            target_sr (int): Target sample rate (default: 16000 Hz).
        
        Returns:
            bytes: Resampled WAV audio as bytes in PCM 16-bit format.
        """
        # Read WAV bytes into NumPy array and detect sample rate
        with io.BytesIO(wav_bytes) as audio_file:
            audio_data, orig_sr = sf.read(audio_file, dtype='int16')  # Read as float32 for precision

        if orig_sr == target_sr:
            return wav_bytes  # No resampling needed
        
        # Compute resampling ratio
        gcd = np.gcd(orig_sr, target_sr)
        up = target_sr // gcd
        down = orig_sr // gcd
        
        resampled_data = sps.resample_poly(audio_data, up, down).astype(np.int16)
        
        with io.BytesIO() as output_file:
            sf.write(output_file, resampled_data, target_sr, format='WAV', subtype='PCM_16')
            return output_file.getvalue()
        
    def get_sample_rate(self, audio_data):
        """Extract sample rate from WAV byte data"""
        with io.BytesIO(audio_data) as audio_file:
            info = sf.info(audio_file)
            return info.samplerate

    def play_audio(self, audio_data):
        """Play audio using PyAudio with support for pause and mute."""
        self.is_turned_on()
        
        audio_data = self.resample_audio(audio_data)
        
        if self._audio_status == 'playing':
            logger.warning("Already playing audio.")
            return

        self._audio_status = 'playing'
        self._pause_event.set()

        def playback():
            logger.info(f"Playing {len(audio_data)} bytes")  # ✅ Debug output
            
            try:
                # Convert bytes to NumPy array (16-bit PCM)
                audio_array = np.frombuffer(audio_data, dtype=np.int16)

                # Apply volume scaling (if volume is between 0-1)
                if not self._muted:
                    scaled_audio = (audio_array * self._volume).astype(np.int16)
                else:
                    scaled_audio = np.zeros_like(audio_array)  # Mute by setting all samples to 0

                # Split the audio into chunks
                for i in range(0, len(scaled_audio), self._chunk_size):
                    while self._audio_status == 'paused':
                        self._pause_event.wait()  # Wait until resumed
                    
                    if self._audio_status == 'stopped':
                        logger.info("Audio playback stopped.")
                        return

                    chunk = scaled_audio[i:i + self._chunk_size].tobytes()
                    self.stream.write(chunk)  # Play the audio chunk

                logger.debug("Playback finished.")  # ✅ Log success
                self._audio_status = 'stopped'

            except Exception as e:
                logger.error(f"SpeakerDevice: Error playing audio: {e}")

        self._thread = threading.Thread(target=playback)
        self._thread.start()

            
    def stop_audio(self):
        """Stop audio from the speaker."""
        self.is_turned_on()
        
        self._audio_status = 'stopped'
        self._pause_event.set()
        self._streaming = False
        return self.get_status(attribute='audio_status')
    
    def pause_audio(self):
        self.is_turned_on()
        
        if self._audio_status == 'playing':
            self._audio_status = 'paused'
            self._pause_event.clear()
        return self.get_status(attribute='audio_status')
    
    def resume_audio(self):
        self.is_turned_on()
        
        if self._audio_status == 'paused':
            self._audio_status = 'playing'
            self._pause_event.set()
        return self.get_status(attribute='audio_status')
    
    def get_status(self, attribute: Optional[Literal['state','device_power', 'muted', 'volume', 'audio_status', 'streaming']]):
        """Get the current status of the speaker."""
        self.is_turned_on()
        
        if attribute:
            return {
                'device_id': self._device_id,
                attribute: getattr(self, f"_{attribute}")
            }
        
        return {
            'device_id': self._device_id,
            'state': self._state,
            'device_power': self._state,
            'muted': self._muted,
            'volume': self._volume,
            'audio_status': self._audio_status,
            'streaming': self._streaming
        }
        
if __name__ == "__main__":
    from openai import OpenAI
    from dotenv import load_dotenv
    from pprint import pprint
    
    logger.info("Testing SpeakerDevice...")
    
    load_dotenv()
    
    client = OpenAI()
    
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input="Today is a wonderful day to build something people love!",
        response_format="wav",
    )
    
    print(type(response.content))
    
    speaker = SpeakerDevice("1")
    speaker.turn_on()
    speaker.play_audio(response.content)