from abc import ABC, abstractmethod

from .base_gateway import BaseGateway

class CameraGateway(BaseGateway):
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
