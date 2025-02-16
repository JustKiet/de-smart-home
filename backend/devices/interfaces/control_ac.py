from abc import ABC, abstractmethod
from backend.devices.interfaces.common.control_power import ControlPower
from backend.devices.interfaces.common.device_status import DeviceStatus
from typing import List, Union, Literal

class ControlAirConditioner(ControlPower,
                            DeviceStatus):
    """Abstract class for air conditioner devices"""


    @abstractmethod
    def set_temperature(self, level):
        """Set the temperature of the air conditioner"""
        pass
    
    @abstractmethod
    def get_temperature(self):
        """Get the temperature of the air conditioner"""
        pass
    
    @abstractmethod
    def set_fan_speed(self, level):
        """Set the fan speed of the air conditioner"""
        pass
    
    @abstractmethod
    def set_humidity(self, level):
        """Set the humidity of the air conditioner"""
        pass
    
    @abstractmethod
    def get_humidity(self):
        """Get the humidity of the air conditioner"""
        pass
    
    @abstractmethod
    def get_fan_speed(self):
        """Get the fan speed of the air conditioner"""
        pass

    @abstractmethod
    def set_mode(self, mode):
        """Set the mode of the air conditioner"""
        pass
    
    @abstractmethod
    def get_mode(self):
        """Get the mode of the air conditioner"""
        pass