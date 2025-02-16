from abc import ABC, abstractmethod

from devices.src.smart_devices.interfaces.common.control_power import ControlPower
from devices.src.smart_devices.interfaces.common.device_status import DeviceStatus

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
