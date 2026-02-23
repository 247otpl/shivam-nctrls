# backend/modules/events/settings_service.py

import json
from pathlib import Path


DEFAULT_SETTINGS = {
    "correlation_window_seconds": 180,
    "suppression_window_seconds": 300
}


def get_settings_path(base_dir, org_id, site_id):

    path = (
        base_dir
        / "data"
        / "orgs"
        / org_id
        / "sites"
        / site_id
        / "settings.json"
    )

    return path


def load_site_settings(base_dir, org_id, site_id):

    path = get_settings_path(base_dir, org_id, site_id)

    if not path.exists():
        return DEFAULT_SETTINGS.copy()

    try:
        data = json.loads(path.read_text())
    except Exception:
        return DEFAULT_SETTINGS.copy()

    # Ensure all required keys exist
    settings = DEFAULT_SETTINGS.copy()
    settings.update(data)

    return settings
