from pydantic import BaseModel


class DeviceMetrics(BaseModel):
    id: int
    x: float
    y: float
    z: float


class Device(BaseModel):
    name: str
    user_id: int


class User(BaseModel):
    login: str
