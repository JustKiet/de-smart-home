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
    
class LightDevices(ControlLight):
    def __init__(self, device_id: int, state: Literal["on", "off"], brightness: int, temperature: float):
        self.lights = []

    def add_light(self, state: Literal["on", "off"], brightness: int, temperature: float):
        light = {"state": state, "brightness": brightness, "temperature": temperature}
        self.lights.append(light)
        return len(self.lights) - 1  # Return the index of the new light

    def turn_on(self, index: int):
        if 0 <= index < len(self.lights):
            self.lights[index]["state"] = "on"
            print(f"Light {index} turned on")

    def turn_off(self, index: int):
        if 0 <= index < len(self.lights):
            self.lights[index]["state"] = "off"
            print(f"Light {index} turned off")

    def set_brightness(self, index: int, level: int):
        if 0 <= index < len(self.lights):
            self.lights[index]["brightness"] = level
            print(f"Brightness of light {index} set to {level}")

    def get_brightness(self, index: int) -> int:
        if 0 <= index < len(self.lights):
            return self.lights[index]["brightness"]
        return 0

    def set_light_temperature(self, index: int, temperature: float):
        if 0 <= index < len(self.lights):
            self.lights[index]["temperature"] = temperature
            print(f"Temperature of light {index} set to {temperature}K")

    def get_light_temperature(self, index: int) -> float:
        if 0 <= index < len(self.lights):
            return self.lights[index]["temperature"]
        return 0.0

class LightGateway:
    def __init__(self, light_devices: List[LightDevices]):
        self.light_devices = {light_device.device_id: light_device for light_device in light_devices}
        
    def log_light_status(self):
        for light_id, light_device in self.light_devices.items():
            print(f"Light {light_id}: {light_device.lights[light_id]} is turned {light_device.lights[light_id]['state']}")
            
    def log_light_brightness(self):
        for light_id, light_device in self.light_devices.items():
            print(f"Light {light_id}: {light_device.lights[light_id]} has brightness {light_device.lights[light_id]['brightness']}")
            
    def log_light_temperature(self):
        for light_id, light_device in self.light_devices.items():
            print(f"Light {light_id}: {light_device.lights[light_id]} has temperature {light_device.lights[light_id]['temperature']}K")
        
    def turn_on_by_id(self, id: Union[int]):
        light_id = 'light_' + str(id)
        if light_id in self.light_devices:
            self.light_devices[light_id].turn_on(light_id)
            self.log_light_status()
        return None
    
    def turn_off_by_id(self, id: Union[int]):
        light_id = 'light_' + str(id)
        if light_id in self.light_devices:
            self.light_devices[light_id].turn_off(light_id)
            self.log_light_status()
        return None
    
    def set_brightness_by_id(self, id: Union[int], level: int):
        light_id = 'light_' + str(id)
        if light_id in self.light_devices:
            self.light_devices[light_id].set_brightness(light_id, level)
            self.log_light_brightness()
        return None
    
    def get_brightness_by_id(self, id: Union[int]) -> int:
        light_id = 'light_' + str(id)
        if light_id in self.light_devices:
            return self.light_devices[light_id].get_brightness(light_id)
        return 0
    
    def set_light_temperature_by_id(self, id: Union[int], temperature: float):
        light_id = 'light_' + str(id)
        if light_id in self.light_devices:
            self.light_devices[light_id].set_light_temperature(light_id, temperature)
            self.log_light_temperature()
        return None
    
    def get_light_temperature_by_id(self, id: Union[int]) -> float:
        light_id = 'light_' + str(id)
        if light_id in self.light_devices:
            return self.light_devices[light_id].get_light_temperature(light_id)
        return 0.0 # 0.0K is absolute zero
    
    


# Example usage
light_devices = LightDevices(0, "on", 100, 3000)
light_gateway = LightGateway([light_devices])
light_gateway.turn_on_by_id(0)
light_gateway.set_brightness_by_id(0, 50)
light_gateway.set_light_temperature_by_id(0, 4000)
light_gateway.turn_off_by_id(0)
light_gateway.get_brightness_by_id(0)
light_gateway.get_light_temperature_by_id(0)
