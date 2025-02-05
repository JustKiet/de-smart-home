from abc import ABC, abstractmethod
from .common.control_base import BaseControl

class ControlAirConditioner(BaseControl):
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
    

class ConcreteAirConditioner(ControlAirConditioner):
    def __init__(self):
        # Default values
        self._temperature = 24
        self._fan_speed = 1
        self._humidity = 50
        self._mode = "cool"

    def set_temperature(self, level):
        self._temperature = level
        print(f"Temperature set to {self._temperature}°C")

    def get_temperature(self):
        return self._temperature

    def set_fan_speed(self, level):
        self._fan_speed = level
        print(f"Fan speed set to {self._fan_speed}")

    def get_fan_speed(self):
        return self._fan_speed

    def set_humidity(self, level):
        self._humidity = level
        print(f"Humidity set to {self._humidity}%")

    def get_humidity(self):
        return self._humidity

    def set_mode(self, mode):
        self._mode = mode
        print(f"Mode set to {self._mode}")

    def get_mode(self):
        return self._mode