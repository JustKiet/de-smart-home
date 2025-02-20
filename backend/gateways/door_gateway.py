from abc import ABC, abstractmethod
from typing import List

# TODO: Rework this class. Wrong directory and wrong naming convention
class HumanCounter(ABC):
    def __init__(self, current_count: int, sensor_status: bool, location: str):
        self.current_count = current_count
        self.sensor_status = sensor_status
        self.location = location

    @abstractmethod
    def activate_counter(self) -> None:
        pass

    @abstractmethod
    def deactivate_counter(self) -> None:
        pass

    @abstractmethod
    def detect_human_entry(self) -> None:
        pass

    @abstractmethod
    def detect_human_exit(self) -> None:
        pass

    @abstractmethod
    def send_count_to_gateway(self) -> None:
        pass

class IdDetection(ABC):
    def __init__(self, detected_id: str, authorized_ids: List[str]):
        self.detected_id = detected_id
        self.authorized_ids = authorized_ids

    @abstractmethod
    def detect_id(self) -> str:
        pass

    @abstractmethod
    def is_authorized(self, id: str) -> bool:
        pass

    @abstractmethod
    def add_authorized_id(self, id: str) -> None:
        pass

    @abstractmethod
    def remove_authorized_id(self, id: str) -> None:
        pass