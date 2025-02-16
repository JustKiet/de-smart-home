from typing import Literal
from devices.src.smart_devices.interfaces.control_light import ControlLight

class LightDevice(ControlLight):
    def __init__(self, device_id):
        self._device_id: str = "light_" + str(device_id)
        self._state: Literal["on", "off"] = "off"
        self._brightness = 100
        self._temperature = 3000
        
    def get_device_id(self):
        return self._device_id
        
    def is_turned_on(self) -> bool:
        if self.state == "on":
            return True
        else:
            raise Exception(f"Light {self.device_id} is turned off. Please turn the device on first.")
        
    def turn_on(self):
        self._state = "on"
        return self.get_status(attribute="state")
        
    def turn_off(self):
        self._state = "off"
        return self.get_status(attribute="state")
        
    def set_brightness(self, level: int):
        self.is_turned_on()       
        self._brightness = level
        return self.get_status(attribute="brightness")
    
    def set_light_temperature(self, temperature: float):
        self.is_turned_on()
        self._temperature = temperature
        return self.get_status(attribute="temperature")
        
    def get_status(self, attribute: Literal["state", "brightness", "temperature"] = None) -> dict:
        self.is_turned_on()
        if attribute:
            return {
                "device_id": self._device_id,
                attribute: getattr(self, f"_{attribute}")
            }
        
        return {
            "device_id": self._device_id,
            "state": self._state,
            "brightness": self._brightness,
            "temperature": self._temperature
        }
        