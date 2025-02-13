from abc import ABC, abstractmethod

from .common.control_base import BaseControl

class ControlCamera(BaseControl):
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
