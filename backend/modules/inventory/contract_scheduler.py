# backend/modules/inventory/contract_scheduler.py

import threading
import time
from pathlib import Path

from .contract_monitor import evaluate_site_contracts
from .contract_notifier import send_contract_notifications


CHECK_INTERVAL_SECONDS = 86400  # 24 hours


class ContractScheduler:

    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.running = False
        self.thread = None

    def start(self):
        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False

    def _run_loop(self):
        while self.running:
            self.run_check()
            time.sleep(CHECK_INTERVAL_SECONDS)

    def run_check(self):
        orgs_path = self.base_dir / "data" / "orgs"

        if not orgs_path.exists():
            return

        for org in orgs_path.iterdir():
            for site in (org / "sites").iterdir():
                result = evaluate_site_contracts(
                    self.base_dir,
                    org.name,
                    site.name
                )

                send_contract_notifications(result)
