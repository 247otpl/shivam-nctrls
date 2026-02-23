# backend/core/execution_planner.py

import json
from pathlib import Path
import uuid


class ExecutionPlanner:

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir

    # -------------------------------------------------
    # INTERNAL HELPERS
    # -------------------------------------------------

    def _get_org_sites_path(self, org_id: str) -> Path:
        return (
            self.base_dir
            / "data"
            / "orgs"
            / org_id
            / "sites"
        )

    def _load_registry(self, org_id: str, site_id: str):

        registry_path = (
            self._get_org_sites_path(org_id)
            / site_id
            / "device_registry.json"
        )

        if not registry_path.exists():
            return []  # Safer than raising error

        with open(registry_path, "r") as f:
            return json.load(f)

    def _is_active(self, device: dict) -> bool:
        return device.get("status", "ACTIVE") == "ACTIVE"

    def _validate_uuid(self, device_id: str):
        try:
            uuid.UUID(device_id)
        except ValueError:
            raise ValueError(f"Invalid device_id format: {device_id}")

    # -------------------------------------------------
    # PUBLIC METHOD
    # -------------------------------------------------

    def get_devices(
        self,
        org_id: str,
        site_id: str = None,
        mode: str = "all",
        device_ids=None,
        mgmt_ips=None,
    ):

        sites_path = self._get_org_sites_path(org_id)

        if not sites_path.exists():
            raise FileNotFoundError(f"Org not found: {org_id}")

        devices = []

        # ---------------------------------------------
        # Mode: all (all sites)
        # ---------------------------------------------
        if mode == "all":

            for site_dir in sites_path.iterdir():
                if site_dir.is_dir():
                    registry = self._load_registry(org_id, site_dir.name)

                    for d in registry:
                        if self._is_active(d):
                            device_copy = d.copy()
                            device_copy["site_id"] = site_dir.name
                            devices.append(device_copy)

            return devices

        # ---------------------------------------------
        # Mode: site
        # ---------------------------------------------
        if mode == "site":

            if not site_id:
                raise ValueError("site_id required for mode=site")

            registry = self._load_registry(org_id, site_id)

            for d in registry:
                if self._is_active(d):
                    device_copy = d.copy()
                    device_copy["site_id"] = site_id
                    devices.append(device_copy)

            return devices

        # ---------------------------------------------
        # Mode: device_ids
        # ---------------------------------------------
        if mode == "device_ids":

            if not device_ids:
                raise ValueError("device_ids required")

            # Validate UUID format
            for dev_id in device_ids:
                self._validate_uuid(dev_id)

            for site_dir in sites_path.iterdir():
                if site_dir.is_dir():
                    registry = self._load_registry(org_id, site_dir.name)

                    for d in registry:
                        if d["device_id"] in device_ids and self._is_active(d):
                            device_copy = d.copy()
                            device_copy["site_id"] = site_dir.name
                            devices.append(device_copy)

            return devices

        # ---------------------------------------------
        # Mode: mgmt_ips
        # ---------------------------------------------
        if mode == "mgmt_ips":

            if not mgmt_ips:
                raise ValueError("mgmt_ips required")

            for site_dir in sites_path.iterdir():
                if site_dir.is_dir():
                    registry = self._load_registry(org_id, site_dir.name)

                    for d in registry:
                        if d["mgmt_ip"] in mgmt_ips and self._is_active(d):
                            device_copy = d.copy()
                            device_copy["site_id"] = site_dir.name
                            devices.append(device_copy)

            return devices

        raise ValueError("Invalid mode")