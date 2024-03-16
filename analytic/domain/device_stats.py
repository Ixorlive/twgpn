from dataclasses import asdict, dataclass
from typing import Dict


@dataclass
class DeviceStats:
    min: float
    max: float
    count: int
    sum: float
    median: float


def device_stats_to_dict(device_stats: DeviceStats) -> Dict:
    return asdict(device_stats)


def dict_to_device_stats(data: Dict) -> DeviceStats:
    return DeviceStats(**data)
