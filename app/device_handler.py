from domain.device import Device
from domain.user import User
from infras.device_repo import DeviceRepo


class DeviceHandler:
    def __init__(self, device_repo: DeviceRepo) -> None:
        self.device_repo = device_repo

    def add_device(self, device: Device):
        return self.device_repo.add_device(device)

    def add_user(self, user: User):
        return self.device_repo.add_user(user)
