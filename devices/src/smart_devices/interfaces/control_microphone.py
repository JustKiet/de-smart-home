from abc import ABC, abstractmethod
from devices.src.smart_devices.interfaces.common.control_power import ControlPower
from devices.src.smart_devices.interfaces.common.device_status import DeviceStatus

class ControlMicrophone(ControlPower,
                        DeviceStatus):
    """An interface for controlling microphone devices.

    Methods:
    - `capture_audio` -- Capture audio from the microphone.
    - `get_audio` -- Get the audio from the microphone.
    - `mute` -- Mute the microphone.
    - `unmute` -- Unmute the microphone
    """
    
    @abstractmethod
    def capture_audio(self):
        raise NotImplementedError
    
    @abstractmethod
    def mute(self):
        raise NotImplementedError
    
    @abstractmethod
    def unmute(self):
        raise NotImplementedError