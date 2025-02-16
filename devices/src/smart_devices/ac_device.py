from devices.src.smart_devices.interfaces.control_ac import ControlAirConditioner
from typing import Literal

class ACDevice(ControlAirConditioner):
    def __init__(self, device_id):
        self._device_id: str = "ac_" + str(device_id)
        self._state: Literal["on", "off"] = "off"
        self._temperature = 24
        self._fan_speed = 1
        self._humidity = 50
        self._mode: Literal["cool", "heat", "dry", "fan", "auto"] = "auto"

    def get_device_id(self):
        return self._device_id
        
    def is_turned_on(self) -> bool:
        if self._state == "on":
            return True
        else:
            raise Exception(f"Air conditioner {self._device_id} is turned off. Please turn the device on first.")
        
    def turn_on(self):
        self._state = "on"
        return self.get_status(attribute="state")
    
    def turn_off(self):
        self._state = "off"
        return self.get_status(attribute="state")
    
    def set_temperature(self, level: float):
        self._temperature = level
        return self.get_status(attribute="temperature")
    
    def set_fan_speed(self, level: int):
        self._fan_speed = level
        return self.get_status(attribute="fan_speed")
    
    def set_humidity(self, level: int):
        self._humidity = level
        return self.get_status(attribute="humidity")
    
    def set_mode(self, mode: str):
        self._mode = mode
        return self.get_status(attribute="mode")
        
    def get_status(self, attribute: Literal["state", "temperature", "fan_speed", "humidity", "mode"] = None) -> dict:
        self.is_turned_on()
        if attribute:
            return {
                "device_id": self._device_id,
                attribute: getattr(self, f"_{attribute}")
            }
            
        return {
            "device_id": self._device_id,
            "state": self._state,
            "temperature": self._temperature,
            "fan_speed": self._fan_speed,
            "humidity": self._humidity,
            "mode": self._mode
        }