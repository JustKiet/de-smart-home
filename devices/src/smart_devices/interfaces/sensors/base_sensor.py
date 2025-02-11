from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, Callable, List
import time

class Sensor(ABC):
    def __init__(self,
                 sensor_id: str,
                 sensor_type: str):
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.last_reading: Optional[Dict[str, Any]] = None
        self.last_updated: float = time.time()
        self._callbacks: List[Callable[[Dict[str, Any]], None]] = []
        
    @abstractmethod
    def read_data(self) -> Dict[str, Any]:
        """
        Abstract method for reading sensor data. Must be implemented by subclasses.
        """
        raise NotImplementedError
    
    def subscribe(self,
                  callback: Callable[[Dict[str, Any]], None]) -> None:
        """
        Registers a callback function to be notified on new sensor data.
        """
        self._callbacks.append(callback)
    
    def notify_subscribers(self) -> None:
        """
        Notifies all subscribers when new sensor data is available.
        """
        for callback in self._callbacks:
            callback(self.last_reading)
            
    def unsubscribe(self,
                    callback: Callable[[Dict[str, Any]], None]) -> None:
        """
        Removes a callback function from the list of subscribers.
        """
        self._callbacks.remove(callback)
    
    def _update_reading(self,
                        value: Any) -> None:
        """
        Updates the sensor reading and notifies subscribers.
        """
        self.last_reading = {
            'sensor_id': self.sensor_id,
            'sensor_type': self.sensor_type,
            'value': value,
            "timestamp": time.time()
        }
        self.last_update = time.time()
        self.notify_subscribers()