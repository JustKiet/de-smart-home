from abc import ABC, abstractmethod
from typing import List, Any
from devices.src.gateways.door.components.door_gateway import HumanCounter, IdDetection

class ControlDoor(ABC):
    def __init__(self, connected_sensors: List[Any], gateway_status: bool):
        self.connected_sensors = connected_sensors
        self.gateway_status = gateway_status

    @abstractmethod
    def process_sensor_data(self, data: Any) -> None:
        pass

    @abstractmethod
    def send_data_to_database(self, data: Any) -> None:
        pass

    @abstractmethod
    def verify_access(self, id: str) -> bool:
        pass

    @abstractmethod
    def log_activity(self, activity: str) -> None:
        pass

    @abstractmethod
    def integrate_human_counter(self, human_counter: HumanCounter) -> None:
        pass

    @abstractmethod
    def integrate_id_detection(self, id_detection: IdDetection) -> None:
        pass