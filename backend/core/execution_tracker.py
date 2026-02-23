# backend/core/execution_tracker.py

import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict


class ExecutionTracker:
    def __init__(self, module_dir: Path):
        self.history_file = module_dir / "execution_history.json"

        if not self.history_file.exists():
            self._init_history()

    # -------------------------------------------------
    def _init_history(self):
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump({"runs": []}, f, indent=4)

    def _load(self) -> Dict:
        with open(self.history_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self, data: Dict):
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    # -------------------------------------------------
    def start_run(self):
        self.start_time = time.time()
        self.run_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    def complete_run(
        self,
        status: str,
        total_devices: int,
        success: int,
        failed: int,
    ):
        duration = round(time.time() - self.start_time, 2)

        data = self._load()

        data["runs"].insert(
            0,
            {
                "run_id": self.run_id,
                "timestamp": self.timestamp,
                "status": status,
                "total_devices": total_devices,
                "success": success,
                "failed": failed,
                "duration_seconds": duration,
            },
        )

        # Keep only last 50 runs
        data["runs"] = data["runs"][:50]

        self._save(data)

    def get_last_run(self):
        data = self._load()
        return data["runs"][0] if data["runs"] else None

    def get_all_runs(self):
        return self._load()["runs"]
