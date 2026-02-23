# backend/core/client_settings.py

import json
from pathlib import Path


DEFAULT_SETTINGS = {
    "ssh_port": 22,
    "telnet_port": 23,
    "timeout": 10
}

def load_client_settings(base_dir: Path, org_id: str, site_id: str, module: str):

    settings_path = (
        base_dir
        / "data"
        / "orgs"
        / org_id
        / "sites"
        / site_id
        / module
        / "settings.json"
    )

    if not settings_path.exists():
        settings_path.parent.mkdir(parents=True, exist_ok=True)

        with open(settings_path, "w") as f:
            json.dump(DEFAULT_SETTINGS, f, indent=4)

        return DEFAULT_SETTINGS

    with open(settings_path, "r") as f:
        return json.load(f)
