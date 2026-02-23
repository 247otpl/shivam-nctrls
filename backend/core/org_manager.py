# backend/core/org_manager.py

import json
import uuid
from datetime import datetime
from pathlib import Path


class OrganisationManager:
    def __init__(self, master_file: Path):
        self.master_file = master_file
        self.master_file.parent.mkdir(parents=True, exist_ok=True)

        if not self.master_file.exists():
            self._write({"organisations": []})

    def _read(self):
        with open(self.master_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write(self, data):
        with open(self.master_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def list(self):
        return self._read()["organisations"]

    def create(self, name: str):
        data = self._read()

        org_id = uuid.uuid4().hex[:8]

        org = {
            "id": org_id,
            "name": name,
            "created_at": datetime.now().isoformat(),
        }

        data["organisations"].append(org)
        self._write(data)

        return org
