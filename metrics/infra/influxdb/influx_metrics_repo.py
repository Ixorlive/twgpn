import json

from domain.device_metrics import DeviceMetrics
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from infra.metrics_repo import MetricsRepo


class InfluxdbMetricsRepo(MetricsRepo):
    def __init__(self) -> None:
        with open("config.json") as f:
            config = json.load(f)

        self.write_client = InfluxDBClient(
            url=config["influx"]["url"],
            token=config["influx"]["token"],
            org=config["influx"]["org"],
        )

    def update_metrics(self, device_metrics: DeviceMetrics):
        json_body = [
            {
                "measurement": "device_metrics",
                "tags": {
                    "device_id": device_metrics.device_id,
                },
                "fields": {
                    "x": device_metrics.x,
                    "y": device_metrics.y,
                    "z": device_metrics.z,
                },
            }
        ]
        write_api = self.write_client.write_api(write_options=SYNCHRONOUS)
        return write_api.write(bucket="devmetrics", org="org", record=json_body)
