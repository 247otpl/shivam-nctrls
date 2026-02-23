# backend\modules\inventory\adapters\base.py

class BaseAdapter:

    def collect_commands(self):
        raise NotImplementedError

    def parse(self, raw_output: str) -> dict:
        raise NotImplementedError
