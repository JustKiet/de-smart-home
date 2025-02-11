from ..interfaces.sensors.base_sensor import Sensor
from typing import Dict, Any
import random

class MotionSensor(Sensor):
    def __init__(self,
                 sensor_id: str,
                 sensor_type: str):
        super().__init__(sensor_id, sensor_type)
        
    def read_data(self) -> Dict[str, Any]:
        """
        Simulates reading data from a motion sensor.
        """
        motion_detected = random.choice([0, 1]) # Mock example
        self._update_reading(motion_detected)
        return self.last_reading
    
class SmartLight:
    def __init__(self, light_id: str):
        self.light_id = light_id

    def motion_trigger(self, sensor_data: Dict[str, Any]):
        if sensor_data["value"] == 1:
            print(f"💡 {self.light_id} turned ON")
        else:
            print(f"💡 {self.light_id} turned OFF")

class SecurityAlarm:
    def __init__(self, alarm_id: str):
        self.alarm_id = alarm_id

    def motion_trigger(self, sensor_data: Dict[str, Any]):
        if sensor_data["value"] == 1:
            print(f"🚨 {self.alarm_id} ALERT! Motion detected!")