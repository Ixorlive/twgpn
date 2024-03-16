from typing import List


class MetricsRepo:
    def get_device_metrics(
        self,
        devices: List[int],
        start_time: str = "-infinity",
        stop_time: str = "now()",
    ):
        raise NotImplementedError
