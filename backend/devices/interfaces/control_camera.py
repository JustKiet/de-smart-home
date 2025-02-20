from abc import ABC, abstractmethod

from backend.devices.interfaces.common.control_power import ControlPower
from backend.devices.interfaces.common.device_status import DeviceStatus

class ControlCamera(ControlPower,
                    DeviceStatus):
    """Abstract class for camera devices"""

    @abstractmethod
    def start_streaming(self):
        """Start streaming video"""
        pass

    @abstractmethod
    def stop_streaming(self):
        """Stop streaming video"""
        pass

    @abstractmethod
    def capture_image(self):
        """Capture an image"""
        pass
