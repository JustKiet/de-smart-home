from abc import ABC, abstractmethod
from devices.src.smart_devices.interfaces.common.control_power import ControlPower
from devices.src.smart_devices.interfaces.common.device_status import DeviceStatus

class ControlGateway(ControlPower,
                     DeviceStatus):
    """Abstract class for gateway devices"""
    pass