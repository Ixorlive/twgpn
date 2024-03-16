from fastapi import APIRouter

from device_handler import DeviceHandler
from domain.device import Device
from domain.user import User
from infras.postgres.psql_device_repo import PsqlDevicesRepo
from routers.models import Device as DeviceModel
from routers.models import User as UserModel

device_mgmt_router = APIRouter()

device_handler = DeviceHandler(PsqlDevicesRepo())


@device_mgmt_router.post("/device")
def update_device(device: DeviceModel):
    id = device_handler.add_device(Device(device.name, device.user_id))
    return {"device id": id}


@device_mgmt_router.post("/user")
def update_user(user: UserModel):
    id = device_handler.add_user(User(user.login))
    return {"user id": id}
