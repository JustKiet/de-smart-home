from abc import ABC, abstractmethod
from datetime import datetime

class DoorSensor(ABC):
    def __init__(self, sensor_status: bool, last_activity_time: datetime):
        self.sensor_status = sensor_status
        self.last_activity_time = last_activity_time

    @abstractmethod
    def activate_sensor(self) -> None:
        pass

    @abstractmethod
    def deactivate_sensor(self) -> None:
        pass

    @abstractmethod
    def detect_door_status(self) -> bool:
        pass

    @abstractmethod
    def send_data_to_gateway(self) -> None:
        pass