from abc import ABC, abstractmethod

class ControlMicrophone(ABC):
    """An interface for controlling microphone devices.

    Methods:
    - `set_sensitivity` -- Set the sensitivity of the microphone.
    - `control_echo` -- Control the echo of the microphone.
    - `capture_audio` -- Capture audio from the microphone.
    - `get_audio` -- Get the audio from the microphone.
    - `mute` -- Mute the microphone.
    - `unmute` -- Unmute the microphone
    """
    @abstractmethod
    def set_sensitivity(self):
        raise NotImplementedError
    
    @abstractmethod
    def control_echo(self):
        raise NotImplementedError
    
    @abstractmethod
    def capture_audio(self):
        raise NotImplementedError
    
    @abstractmethod
    def get_audio(self):
        raise NotImplementedError
    
    @abstractmethod
    def mute(self):
        raise NotImplementedError
    
    @abstractmethod
    def unmute(self):
        raise NotImplementedError