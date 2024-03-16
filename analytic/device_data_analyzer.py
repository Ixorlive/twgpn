import statistics
from typing import Dict, List

from domain.device_stats import DeviceStats
from infras.device_repo import DeviceRepo
from infras.metrics_repo import MetricsRepo


class DeviceDataAnalyzer:
    def __init__(self, metrics_repo: MetricsRepo, devices_repo: DeviceRepo) -> None:
        self.metrics_repo = metrics_repo
        self.devices_repo = devices_repo

    def _get_device_metrics(
        self,
        devices: List[int],
        start_time,
        stop_time,
    ) -> dict:
        return self.metrics_repo.get_device_metrics(devices, start_time, stop_time)

    def _calculate_stats(self, vals: List[float]) -> DeviceStats:
        return DeviceStats(
            min(vals), max(vals), len(vals), sum(vals), statistics.median(vals)
        )

    def get_device_stats(
        self,
        device_id: int,
        metric_key: str = "x",
        start_time: str = "1970-01-01T00:00:00Z",
        stop_time: str = "",
    ) -> DeviceStats:
        metrics = self._get_device_metrics([device_id], start_time, stop_time)
        if device_id not in metrics or not metrics[device_id]:
            raise ValueError(f"No data found for device with id: {device_id}")

        metric_values = [
            metric[metric_key] for metric in metrics[device_id] if metric_key in metric
        ]
        return self._calculate_stats(metric_values)

    def get_user_metrics_all(
        self,
        user_id: int,
        metric_key: str = "x",
        start_time: str = "1970-01-01T00:00:00Z",
        stop_time: str = "",
    ) -> DeviceStats:
        user_devices = self.devices_repo.get_devices_by_user(user_id)
        if user_devices is None:
            raise ValueError(f"User with id ${user_id} not found")
        devices_metrics = self._get_device_metrics(user_devices, start_time, stop_time)
        metrics_all = [
            metric[metric_key]
            for dev_metrics in devices_metrics
            for metric in dev_metrics
        ]
        return self._calculate_stats(metrics_all)

    def get_user_metrics_foreach(
        self,
        user_id: int,
        metric_key: str = "x",
        start_time: str = "1970-01-01T00:00:00Z",
        stop_time: str = "",
    ) -> Dict:
        user_devices = self.devices_repo.get_devices_by_user(user_id)
        if user_devices is None:
            raise ValueError(f"User with id ${user_id} not found")
        devices_metrics = self._get_device_metrics(user_devices, start_time, stop_time)
        return {
            device_id: self._calculate_stats(metric[metric_key])
            for device_id, dev_metrics in devices_metrics.items()
            for metric in dev_metrics
        }
