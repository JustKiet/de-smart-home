from abc import ABC, abstractmethod

class FingerprintSensor(ABC):
    def __init__(self, sensor_status: bool, last_detect_id: str, enrolled_fingerprints: list):
        self.sensor_status = sensor_status
        self.last_detect_id = last_detect_id
        self.enrolled_fingerprints = enrolled_fingerprints

    @abstractmethod
    def activate_sensor(self) -> None:
        pass

    @abstractmethod
    def deactivate_sensor(self) -> None:
        pass

    @abstractmethod
    def scan_fingerprint(self) -> str:
        pass

    @abstractmethod
    def enroll_fingerprint(self, id: str) -> bool:
        pass

    @abstractmethod
    def verify_fingerprint(self, id: str) -> bool:
        pass