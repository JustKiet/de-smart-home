from abc import ABC, abstractmethod
from typing import List

# TODO: Rework this class. Wrong directory and wrong naming convention

class Frame:
    # Assuming Frame is a predefined class
    pass

class User:
    # Assuming User is a predefined class
    pass

class LogData:
    # Assuming LogData is a predefined class
    pass

class Event:
    # Assuming Event is a predefined class
    pass

class AllResult:
    # Assuming AllResult is a predefined class
    pass

class Camera:
    # Assuming Camera is a predefined class
    pass

class RawVideo:
    # Assuming RawVideo is a predefined class
    pass


class ActivityDetector(ABC):
    def __init__(self, current_frame: Frame, user_data: User):
        self.current_frame = current_frame
        self.user_data = user_data

    @abstractmethod
    def detect_activity(self) -> bool:
        pass

    @abstractmethod
    def classify_user(self) -> str:
        pass
    
    

class FrameProcessor(ABC):
    def __init__(self, frame_log: List[Frame]):
        self.frame_log = frame_log

    @abstractmethod
    def process_frame(self) -> None:
        pass

    @abstractmethod
    def store_log(self, log_data: LogData) -> bool:
        pass

    @abstractmethod
    def request_all_processing(self, event: Event) -> AllResult:
        pass
    
    
class CameraManager(ABC):
    def __init__(self, manage_camera: List[Camera]):
        self.manage_camera = manage_camera

    @abstractmethod
    def add_camera(self, camera: Camera) -> None:
        pass

    @abstractmethod
    def remove_camera(self, camera_id: str) -> None:
        pass

    @abstractmethod
    def update_camera_settings(self, camera_id: str, command: str) -> None:
        pass

    @abstractmethod
    def send_to_activity_detection(self, raw_video: RawVideo) -> None:
        pass