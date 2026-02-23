# backend/core/site_manager.py

import json
import uuid
from datetime import datetime
from pathlib import Path


class SiteManager:
    def __init__(self, org_dir: Path):
        self.sites_file = org_dir / "sites.json"

        if not self.sites_file.exists():
            self._write({"sites": []})

    def _read(self):
        with open(self.sites_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write(self, data):
        with open(self.sites_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def list(self):
        return self._read()["sites"]

    def create(self, name: str):
        data = self._read()

        site_id = uuid.uuid4().hex[:8]

        site = {
            "id": site_id,
            "name": name,
            "created_at": datetime.now().isoformat(),
        }

        data["sites"].append(site)
        self._write(data)

        return site
