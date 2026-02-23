# backend/core/logging/base_logger.py

from pathlib import Path
from datetime import datetime, timezone
import json
import uuid


def utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class BaseLogger:

    def __init__(self, base_dir, org_id, site_id, module):
        self.base_dir = base_dir
        self.org_id = org_id
        self.site_id = site_id
        self.module = module

        # UUID based run_id (safer than timestamp)
        self.run_id = str(uuid.uuid4())

        self.site_dir = (
            base_dir
            / "data"
            / "orgs"
            / org_id
            / "sites"
            / site_id
        )

        self.module_dir = self.site_dir / module

        self.results = []
        self.metadata = {
            "run_id": self.run_id,
            "module": module,
            "org_id": org_id,
            "site_id": site_id,
            "status": "PENDING",
            "start_time": utc_now(),
        }

    def add_device_result(self, device_id, status, error=None, extra=None):

        entry = {
            "device_id": device_id,
            "status": status,
        }

        if error:
            entry["error"] = error

        if extra:
            entry.update(extra)

        self.results.append(entry)

    def finalize(self):
        self.metadata["end_time"] = utc_now()
        self.metadata["status"] = "COMPLETED"
        self.metadata["total_devices"] = len(self.results)
        self.metadata["results"] = self.results

        self.write_log()

    def write_log(self):
        raise NotImplementedError("write_log() must be implemented by child logger")