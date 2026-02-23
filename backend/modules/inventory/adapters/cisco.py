# backend\modules\inventory\adapters\cisco.py

from .base import BaseAdapter


class CiscoAdapter(BaseAdapter):

    def collect_commands(self):
        return ["show version", "show inventory"]

    def parse(self, raw_output: str):

        data = {
            "hostname": "",
            "vendor": "cisco",
            "platform": "",
            "model": "",
            "serial_number": "",
            "os_version": "",
            "hardware_version": ""
        }

        for line in raw_output.splitlines():

            if "Cisco IOS XE Software" in line:
                data["platform"] = "ios-xe"

            if "Processor board ID" in line:
                data["serial_number"] = line.split()[-1]

            if "Model number" in line:
                data["model"] = line.split(":")[-1].strip()

            if "Version" in line and "Cisco IOS" in line:
                data["os_version"] = line.strip()

        return data
