# backend\modules\inventory\adapters\allied.py

from .base import BaseAdapter


class AlliedAdapter(BaseAdapter):

    def collect_commands(self):
        return ["show system"]

    def parse(self, raw_output: str):

        data = {
            "hostname": "",
            "vendor": "allied-telesis",
            "platform": "alliedware-plus",
            "model": "",
            "serial_number": "",
            "os_version": "",
            "hardware_version": ""
        }

        for line in raw_output.splitlines():

            if "Board Name" in line:
                parts = line.split()
                data["model"] = parts[-2]

            if "Serial number" in line:
                data["serial_number"] = line.split()[-1]

            if "Software version" in line:
                data["os_version"] = line.split(":")[-1].strip()

        return data
