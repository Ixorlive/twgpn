from contextlib import closing

import psycopg2

from infras.device_repo import DeviceRepo


class PsqlDevicesRepo(DeviceRepo):
    def __init__(self):
        super().__init__()
        self.conn = psycopg2.connect(
            dbname="devices_db", user="postgres", password="example", host="localhost"
        )

    def get_devices_by_user(self, user_id):
        with closing(self.conn.cursor()) as cur:
            cur.execute("SELECT id FROM devices WHERE user_id=%s;", (user_id,))
            devices = cur.fetchall()
            device_ids = [device[0] for device in devices]
            return device_ids
