from abc import ABC, abstractmethod
from typing import Any

class Camera(ABC):
    """Abstract class for camera devices"""
    def __init__(self, id: int, resolution: str, frame_rate: int):
        self.id = id
        self.resolution = resolution
        self.frame_rate = frame_rate

    @abstractmethod
    def capture_image(self) -> Any:
        """Capture an image"""
        pass

    @abstractmethod
    def detect_person(self) -> bool:
        """Detect a person in the image"""
        pass

    @abstractmethod
    def analyze_environment(self) -> str:
        """Analyze the environment"""
        pass