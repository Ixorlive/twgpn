import json
from contextlib import closing

import psycopg2

from infras.device_repo import DeviceRepo


class PsqlDevicesRepo(DeviceRepo):
    def __init__(self):
        with open("config.json") as f:
            config = json.load(f)

        self.conn = psycopg2.connect(
            dbname=config["postgres"]["dbname"],
            user=config["postgres"]["user"],
            password=config["postgres"]["password"],
            host=config["postgres"]["host"],
        )

    def get_devices_by_user(self, user_id):
        with closing(self.conn.cursor()) as cur:
            cur.execute("SELECT id FROM devices WHERE user_id=%s;", (user_id,))
            devices = cur.fetchall()
            device_ids = [device[0] for device in devices]
            return device_ids
