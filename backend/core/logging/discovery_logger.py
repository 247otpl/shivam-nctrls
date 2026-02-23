# backend/core/logging/discovery_logger.py

from pathlib import Path
import json
from .base_logger import BaseLogger
from .retention_manager import RetentionManager


class DiscoveryLogger(BaseLogger):

    def __init__(self, base_dir, org_id, site_id):
        super().__init__(base_dir, org_id, site_id, "discovery")

        self.log_dir = self.module_dir / "logs"
        self.scan_dir = self.module_dir / "scans" / self.run_id

        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.scan_dir.mkdir(parents=True, exist_ok=True)

        self.retention = RetentionManager(self.module_dir)

    def write_log(self):

        # Save metadata inside scan folder
        metadata_file = self.scan_dir / "scan_metadata.json"

        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, indent=4)

        # Also save summary log
        log_file = self.log_dir / f"{self.run_id}.json"

        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, indent=4)

        self.retention.cleanup_logs(self.log_dir)