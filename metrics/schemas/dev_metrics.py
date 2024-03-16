from pydantic import BaseModel


class DevMetrics(BaseModel):
    device_id: int
    x: float
    y: float
    z: float
