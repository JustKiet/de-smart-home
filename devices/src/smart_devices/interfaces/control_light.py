from abc import ABC, abstractmethod
from typing import List, Union, Literal
# from .common.control_base import BaseControl

class ControlLight(ABC):
    """Abstract class for light devices"""

    @abstractmethod
    def turn_on(self, light_id: int):
        """Turn on the light"""
        pass

    @abstractmethod
    def turn_off(self, light_id: int):
        """Turn off the light"""
        pass

    @abstractmethod
    def set_brightness(self, light_id: int, level: int):
        """Set the brightness of the light"""
        pass
    
    @abstractmethod
    def get_brightness(self, light_id: int) -> int:
        """Get the brightness of the light"""
        pass
    
    @abstractmethod
    def set_light_temperature(self, light_id: int, temperature: float):
        """Set the temperature of the light"""
        pass
    
    @abstractmethod
    def get_light_temperature(self, light_id: int) -> float:
        """Get the temperature of the light"""
        pass