# backend/modules/events/device_resolver.py

import json
from pathlib import Path


def resolve_device(base_dir, source_ip):

    orgs_path = base_dir / "data" / "orgs"

    if not orgs_path.exists():
        return None

    for org in orgs_path.iterdir():
        sites_path = org / "sites"
        if not sites_path.exists():
            continue

        for site in sites_path.iterdir():
            registry = site / "device_registry.json"
            if not registry.exists():
                continue

            devices = json.loads(registry.read_text())

            for device in devices:
                if device.get("mgmt_ip") == source_ip:
                    return {
                        "org_id": org.name,
                        "site_id": site.name,
                        "device_id": device["device_id"]
                    }

    return None