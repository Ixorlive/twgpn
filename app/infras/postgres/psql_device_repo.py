from contextlib import closing

import psycopg2

from domain.device import Device
from domain.user import User
from infras.device_repo import DeviceRepo


class PsqlDevicesRepo(DeviceRepo):
    def __init__(self):
        super().__init__()
        self.conn = psycopg2.connect(
            dbname="devices_db", user="postgres", password="example", host="localhost"
        )

    def add_user(self, user: User):
        with closing(self.conn.cursor()) as cur:
            cur.execute(
                "INSERT INTO Users (login) VALUES (%s) RETURNING id;", (user.login,)
            )
            user_id = cur.fetchone()
            self.conn.commit()
            return user_id[0]

    def add_device(self, device: Device):
        with closing(self.conn.cursor()) as cur:
            cur.execute(
                "INSERT INTO Devices (name, user_id) VALUES (%s, %s) RETURNING id;",
                (device.name, device.user_id),
            )
            device_id = cur.fetchone()
            self.conn.commit()
            return device_id[0]
