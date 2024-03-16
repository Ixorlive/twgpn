import json
from typing import List

from influxdb_client import InfluxDBClient

from infras.metrics_repo import MetricsRepo


class InfluxdbMetricsRepo(MetricsRepo):
    def __init__(self) -> None:
        with open("config.json") as f:
            config = json.load(f)

        self.write_client = InfluxDBClient(
            url=config["influx"]["url"],
            token=config["influx"]["token"],
            org=config["influx"]["org"],
        )
        self.query_api = self.write_client.query_api()

    def get_device_metrics(
        self,
        devices: List[int],
        start_time: str = "1970-01-01T00:00:00Z",
        stop_time: str = "",
    ) -> dict:
        """
        Retrieves metrics for a list of devices over a given time period.

        :param devices: List of device IDs.
        :param start_time: Start time for the metrics query in RFC3339 format. Defaults to
                           the Unix epoch start if not specified.
        :param stop_time: End time for the metrics query in RFC3339 format. If not specified,
                          the query will include all records up until the current time.
        :return: A dictionary where keys are device IDs and values are lists of metrics
                 records.
        """
        results = {}
        print(devices, start_time, stop_time)

        for device_id in devices:
            # Constructing the range part of the query based on start and stop times
            range_part = f"start: {start_time}"
            if stop_time:  # Only add the stop part if stop_time is not empty
                range_part += f", stop: {stop_time}"

            # Construct the complete Flux query
            query = f"""
                from(bucket: "devmetrics")
                |> range({range_part})
                |> filter(fn: (r) => r["_measurement"] == "device_metrics")
                |> filter(fn: (r) => r["device_id"] == "{device_id}")
                |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
            """
            result = self.query_api.query(query)

            device_results = []
            for table in result:
                for record in table.records:
                    device_results.append(
                        {
                            "x": record["x"],
                            "y": record["y"],
                            "z": record["z"],
                        }
                    )
            results[device_id] = device_results

        return results
