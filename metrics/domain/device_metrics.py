from dataclasses import dataclass


@dataclass
class DeviceMetrics:
    device_id: int
    x: float
    y: float
    z: float
