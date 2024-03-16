from domain.device_metrics import DeviceMetrics
from fastapi import FastAPI
from infra.influxdb.influx_metrics_repo import InfluxdbMetricsRepo
from schemas.dev_metrics import DevMetrics

app = FastAPI()

repo = InfluxdbMetricsRepo()


@app.get("/")
def read_root():
    """
    A simple entry point to return a greeting message.
    """
    return {
        "message": "Send your data from device here! We process data as soon as possible"
    }


@app.post("/stats")
def send_metrics(metrics: DevMetrics):
    """
    Receiving statistics from various devices and adding them to queue to the message broker
    """
    repo.update_metrics(
        DeviceMetrics(metrics.device_id, metrics.x, metrics.y, metrics.z)
    )
    return {"message": "metrics updated"}
