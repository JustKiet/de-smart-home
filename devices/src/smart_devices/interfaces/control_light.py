from abc import ABC, abstractmethod
from .common.control_base import BaseControl

class LightGateway(BaseControl):
    """Abstract class for light devices"""

    @abstractmethod
    def turn_on(self):
        """Turn on the light"""
        pass

    @abstractmethod
    def turn_off(self):
        """Turn off the light"""
        pass

    @abstractmethod
    def set_brightness(self, level):
        """Set the brightness of the light"""
        pass
