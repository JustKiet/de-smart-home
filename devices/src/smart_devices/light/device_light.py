from typing import Literal

from devices.src.smart_devices.interfaces.control_light import ControlLight
class LightDevice(ControlLight):
    def __init__(self, device_id):
        self.device_id: str = "light_" + str(device_id)
        self.state: Literal["on", "off"] = "off"
        self.brightness = 100
        self.temperature = 3000
        
    def turn_on(self, light_id: int):
        self.state = "on"
        print(f"Light {self.device_id} turned on")
        
    def turn_off(self, light_id: int):
        self.state = "off"
        print(f"Light {self.device_id} turned off")
        
    def set_brightness(self, light_id: int, level: int):
        self.brightness = level
        print(f"Brightness of light {self.device_id} set to {self.brightness}")
        
    def get_brightness(self, light_id: int) -> int:
        return self.brightness
    
    def set_light_temperature(self, light_id: int, temperature: float):
        self.temperature = temperature
        print(f"Temperature of light {self.device_id} set to {self.temperature}K")
        
    def get_light_temperature(self, light_id: int) -> float:
        return self.temperature
    
    def update(self):
        return "Updated to the latest version."

    def rollback(self):
        return "Rolled back to the previous version."