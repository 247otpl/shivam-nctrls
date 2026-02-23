# backend/core/org_service.py

import json
from pathlib import Path
from typing import Dict, List


class OrgService:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.data_dir = self.base_dir / "data"
        self.master_file = self.data_dir / "master.json"

        self.data_dir.mkdir(exist_ok=True)
        if not self.master_file.exists():
            self._init_master()

    # -------------------------------------------------
    # INTERNAL
    # -------------------------------------------------
    def _init_master(self):
        with open(self.master_file, "w", encoding="utf-8") as f:
            json.dump({"organisations": []}, f, indent=4)

    def _load(self) -> Dict:
        if not self.master_file.exists() or self.master_file.stat().st_size == 0:
            self._init_master()

        try:
            with open(self.master_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            # Auto-recover corrupted file
            self._init_master()
            return {"organisations": []}

    def _save(self, data: Dict):
        with open(self.master_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    # -------------------------------------------------
    # ORG OPERATIONS
    # -------------------------------------------------
    def create_org(self, org_id: str, name: str):
        data = self._load()

        for org in data["organisations"]:
            if org["org_id"] == org_id:
                raise ValueError("Organisation already exists")

        new_org = {
            "org_id": org_id,
            "name": name,
            "sites": []
        }

        data["organisations"].append(new_org)
        self._save(data)

        # Physically create org folder
        org_dir = self.data_dir / "orgs" / org_id
        org_dir.mkdir(parents=True, exist_ok=True)

    def list_orgs(self) -> List[Dict]:
        return self._load()["organisations"]

    # -------------------------------------------------
    # SITE OPERATIONS
    # -------------------------------------------------
    def create_site(self, org_id: str, site_id: str, name: str):
        data = self._load()

        for org in data["organisations"]:
            if org["org_id"] == org_id:
                for site in org["sites"]:
                    if site["site_id"] == site_id:
                        raise ValueError("Site already exists")

                org["sites"].append({
                    "site_id": site_id,
                    "name": name
                })
                self._save(data)

                # Create site directory physically
                site_dir = (
                    self.data_dir
                    / "orgs"
                    / org_id
                    / "sites"
                    / site_id
                )
                site_dir.mkdir(parents=True, exist_ok=True)

                return

        raise ValueError("Organisation not found")

    def list_sites(self, org_id: str) -> List[Dict]:
        data = self._load()
        for org in data["organisations"]:
            if org["org_id"] == org_id:
                return org["sites"]

        raise ValueError("Organisation not found")

    # -------------------------------------------------
    # VALIDATION
    # -------------------------------------------------
    def validate(self, org_id: str, site_id: str):
        data = self._load()

        for org in data["organisations"]:
            if org["org_id"] == org_id:
                for site in org["sites"]:
                    if site["site_id"] == site_id:
                        return True
                raise ValueError("Site not registered")

        raise ValueError("Organisation not registered")
