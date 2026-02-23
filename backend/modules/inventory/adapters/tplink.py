# backend\modules\inventory\adapters\tplink.py

from .base import BaseAdapter


class TPLinkAdapter(BaseAdapter):

    def collect_commands(self):
        return ["show system-info"]

    def parse(self, raw_output: str):

        data = {
            "hostname": "",
            "vendor": "tp-link",
            "platform": "",
            "model": "",
            "serial_number": "",
            "os_version": "",
            "hardware_version": ""
        }

        for line in raw_output.splitlines():

            if "System Name" in line:
                data["hostname"] = line.split("-")[-1].strip()

            if "Hardware Version" in line:
                data["hardware_version"] = line.split("-")[-1].strip()

            if "Software Version" in line:
                data["os_version"] = line.split("-")[-1].strip()

            if "Serial Number" in line:
                data["serial_number"] = line.split("-")[-1].strip()

        return data
