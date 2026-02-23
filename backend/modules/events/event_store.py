# backend/modules/events/event_store.py

import json
from pathlib import Path
from datetime import datetime, timedelta


DATE_FORMAT = "%d-%m-%Y %H:%M:%S"
FILE_DATE_FORMAT = "%d-%m-%Y"


def _now_str():
    return datetime.now().strftime(DATE_FORMAT)


def _parse_time(timestr):
    return datetime.strptime(timestr, DATE_FORMAT)


def _get_event_file(base_dir, org_id, site_id):

    today = datetime.now().strftime(FILE_DATE_FORMAT)

    path = (
        base_dir
        / "data"
        / "orgs"
        / org_id
        / "sites"
        / site_id
        / "events"
        / f"{today}.json"
    )

    path.parent.mkdir(parents=True, exist_ok=True)

    if not path.exists():
        path.write_text("[]")

    return path


def store_event(base_dir, org_id, site_id, event):

    path = _get_event_file(base_dir, org_id, site_id)
    events = json.loads(path.read_text())

    event["recorded_at"] = _now_str()
    events.append(event)

    path.write_text(json.dumps(events, indent=4))


def load_recent_events(
    base_dir,
    org_id,
    site_id,
    device_id,
    window_seconds
):

    path = _get_event_file(base_dir, org_id, site_id)
    events = json.loads(path.read_text())

    now = datetime.now()
    cutoff = now - timedelta(seconds=window_seconds)

    filtered = []

    for event in events:

        if event.get("device_id") != device_id:
            continue

        event_time = _parse_time(event["timestamp"])

        if event_time >= cutoff:
            filtered.append(event)

    return filtered
C