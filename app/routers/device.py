from typing import Dict

from fastapi import APIRouter, Body, Response, status

from device_handler import DeviceHandler
from domain.device import Device
from domain.user import User
from infras.postgres.psql_device_repo import PsqlDevicesRepo
from routers.models import Device as DeviceModel
from routers.models import User as UserModel

device_mgmt_router = APIRouter()

device_handler = DeviceHandler(PsqlDevicesRepo())


@device_mgmt_router.post(
    "/device",
    response_model=Dict[str, int],
    status_code=status.HTTP_201_CREATED,
    summary="Add a new device",
    description="This endpoint adds a new device to the system. You need to provide a device model which includes the device name and user ID.",
)
def add_device(
    device: DeviceModel = Body(..., example={"name": "DeviceName", "user_id": 1234})
):
    """
    Add a new device to the system.

    - **name**: The name of the device.
    - **user_id**: The ID of the user associated with this device.
    """
    id = device_handler.add_device(Device(device.name, device.user_id))
    return Response(content={"device id": id}, status_code=status.HTTP_201_CREATED)


@device_mgmt_router.post(
    "/user",
    response_model=Dict[str, int],
    status_code=status.HTTP_201_CREATED,
    summary="Add a new user",
    description="This endpoint adds a new user to the system. You need to provide a user model which includes the login details.",
)
def add_user(user: UserModel = Body(..., example={"login": "userLogin"})):
    """
    Add a new user to the system.

    - **login**: The login of the user.
    """
    id = device_handler.add_user(User(user.login))
    return Response(content={"user id": id}, status_code=status.HTTP_201_CREATED)
