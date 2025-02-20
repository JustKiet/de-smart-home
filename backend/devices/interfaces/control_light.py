from abc import ABC, abstractmethod
from typing import List, Union, Literal
from backend.devices.interfaces.common.control_power import ControlPower
from backend.devices.interfaces.common.device_status import DeviceStatus

class ControlLight(ControlPower,
                   DeviceStatus):
    """Abstract class for light devices"""

    @abstractmethod
    def set_brightness(self, light_id: int, level: int):
        """Set the brightness of the light"""
        raise NotImplementedError
    
    @abstractmethod
    def set_light_temperature(self, light_id: int, temperature: float):
        """Set the temperature of the light"""
        raise NotImplementedError
    