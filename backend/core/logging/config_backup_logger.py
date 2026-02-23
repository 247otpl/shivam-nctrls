from pathlib import Path
import json
from .base_logger import BaseLogger
from .retention_manager import RetentionManager


class ConfigBackupLogger(BaseLogger):

    def __init__(self, base_dir, org_id, site_id):
        super().__init__(base_dir, org_id, site_id, "config_backup")

        self.execution_log_dir = self.module_dir / "execution_logs"
        self.execution_log_dir.mkdir(parents=True, exist_ok=True)
        self.retention = RetentionManager(self.module_dir)
        self.retention.cleanup_logs(self.execution_log_dir)

    def write_log(self):
        log_file = self.execution_log_dir / f"{self.run_id}.json"

        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, indent=4)
