# backend\modules\inventory\adapters\generic.py

from .base import BaseAdapter


class GenericAdapter(BaseAdapter):

    def collect_commands(self):
        return ["show version"]

    def parse(self, raw_output: str):

        return {
            "hostname": "",
            "vendor": "unknown",
            "platform": "",
            "model": "",
            "serial_number": "",
            "os_version": "",
            "hardware_version": ""
        }
