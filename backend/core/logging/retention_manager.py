# backend/core/logging/retention_manager.py

from pathlib import Path
from datetime import datetime, timedelta
import json


class RetentionManager:

    def __init__(self, module_dir: Path):
        self.module_dir = module_dir
        self.settings_file = module_dir / "settings.json"

        self.retention_days = None
        self.max_runs = None

        self.load_settings()

    def load_settings(self):
        if not self.settings_file.exists():
            return

        data = json.loads(self.settings_file.read_text())

        self.retention_days = data.get("retention_days")
        self.max_runs = data.get("max_runs")

    # -------------------------------------------------
    # CLEANUP LOG FILES
    # -------------------------------------------------
    def cleanup_logs(self, log_dir: Path):

        if not log_dir.exists():
            return

        files = sorted(
            log_dir.glob("*.json"),
            key=lambda f: f.stat().st_mtime,
            reverse=True
        )

        # Apply max_runs
        if self.max_runs and len(files) > self.max_runs:
            for old_file in files[self.max_runs:]:
                old_file.unlink()

        # Apply retention_days
        if self.retention_days:
            cutoff = datetime.now() - timedelta(days=self.retention_days)

            for file in log_dir.glob("*.json"):
                if datetime.fromtimestamp(file.stat().st_mtime) < cutoff:
                    file.unlink()

    # -------------------------------------------------
    # CLEANUP OUTPUT FOLDERS
    # -------------------------------------------------
    def cleanup_output_runs(self, output_dir: Path):

        if not output_dir.exists():
            return

        folders = sorted(
            [f for f in output_dir.iterdir() if f.is_dir()],
            key=lambda f: f.stat().st_mtime,
            reverse=True
        )

        if self.max_runs and len(folders) > self.max_runs:
            for old_folder in folders[self.max_runs:]:
                for item in old_folder.glob("*"):
                    item.unlink()
                old_folder.rmdir()
