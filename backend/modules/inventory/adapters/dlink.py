# backend\modules\inventory\adapters\dlink.py

from .base import BaseAdapter


class DLinkAdapter(BaseAdapter):

    def collect_commands(self):
        return ["show unit"]

    def parse(self, raw_output: str):

        data = {
            "hostname": "",
            "vendor": "d-link",
            "platform": "",
            "model": "",
            "serial_number": "",
            "os_version": "",
            "hardware_version": ""
        }

        for line in raw_output.splitlines():

            if "Model Name" in line:
                data["model"] = line.split()[-1]

            if "Serial-Number" in line:
                parts = line.split()
                if len(parts) > 1:
                    data["serial_number"] = parts[1]

        return data
