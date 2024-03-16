from domain.device_metrics import DeviceMetrics
from fastapi import Body, FastAPI, status
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


@app.post(
    "/stats",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Send device metrics",
    description="This endpoint updates the device metrics in the database (e.g., InfluxDB). \
        You need to provide the device metrics model, including device ID and metrics data.",
)
def send_metrics(
    metrics: DevMetrics = Body(
        ..., example={"device_id": "1", "x": 1.0, "y": 2.0, "z": 3.0}
    )
):
    """
    Updates device metrics in the database.

    - **device_id**: Unique identifier for the device.
    - **x**: The x metric value for the device.
    - **y**: The y metric value for the device.
    - **z**: The z metric value for the device.
    """
    repo.update_metrics(
        DeviceMetrics(metrics.device_id, metrics.x, metrics.y, metrics.z)
    )
    return {"message": "updated"}
