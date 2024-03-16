from typing import Dict

from celery import Celery
from device_data_analyzer import DeviceDataAnalyzer
from domain.device_stats import device_stats_to_dict
from infras.influxdb.influx_metrics_repo import InfluxdbMetricsRepo
from infras.postgres.psql_devices_repo import PsqlDevicesRepo

app = Celery("metrics")
app.config_from_object("celery_config")


metrics_repo = InfluxdbMetricsRepo()
devices_repo = PsqlDevicesRepo()
device_data_analyzer = DeviceDataAnalyzer(metrics_repo, devices_repo)


@app.task(name="dev_stats", queue="dev_metrics")
def dev_metrics_by_device_id(
    device_id: int, metric_key: str, start_time: str, stop_time: str
) -> Dict:
    stats = device_data_analyzer.get_device_stats(
        device_id, metric_key, start_time, stop_time
    )
    return device_stats_to_dict(stats)


@app.task(name="user_stats_all", queue="user_all")
def dev_metrics_by_user_all(
    user_id: int, metric_key: str, start_time: str, stop_time: str
) -> Dict:
    stats = device_data_analyzer.get_user_metrics_all(
        user_id, metric_key, start_time, stop_time
    )
    return device_stats_to_dict(stats)


@app.task(name="useк_stats_foreach", queue="user_foreach")
def dev_metrics_by_user_foreach(
    user_id: int, metric_key: str, start_time: str, stop_time: str
) -> Dict[int, Dict]:
    stats = device_data_analyzer.get_user_metrics_foreach(
        user_id, metric_key, start_time, stop_time
    )
    return {
        device_id: device_stats_to_dict(stats) for device_id, stats in stats.items()
    }
