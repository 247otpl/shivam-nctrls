# backend/modules/events/alert_store.py

import json
import uuid
from pathlib import Path
from datetime import datetime

from .settings_service import load_site_settings
from .correlation.engine import analyze


SEVERITY_SCORES = {
    "INFO": 1,
    "MINOR": 2,
    "MAJOR": 3,
    "CRITICAL": 4,
    "FATAL": 5
}


# -------------------------------------------------
# Utility Functions
# -------------------------------------------------

def _now_str():
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")


def _parse_time(timestr):
    return datetime.strptime(timestr, "%d-%m-%Y %H:%M:%S")


def _format_duration(seconds):

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    return f"{hours:02}:{minutes:02}:{secs:02}"


# -------------------------------------------------
# File Handling
# -------------------------------------------------

def _get_alert_file(base_dir, org_id, site_id):

    today = datetime.now().strftime("%d-%m-%Y")

    path = (
        base_dir
        / "data"
        / "orgs"
        / org_id
        / "sites"
        / site_id
        / "alerts"
        / f"{today}.json"
    )

    path.parent.mkdir(parents=True, exist_ok=True)

    if not path.exists():
        path.write_text("[]")

    return path


def _load_alerts(path):
    return json.loads(path.read_text())


def _save_alerts(path, alerts):
    path.write_text(json.dumps(alerts, indent=4))


# -------------------------------------------------
# Alert Creation / Update
# -------------------------------------------------
def create_or_update_alert(
    base_dir,
    org_id,
    site_id,
    device_id,
    alert_type,
    base_severity
):

    settings = load_site_settings(base_dir, org_id, site_id)
    suppression_window = settings["suppression_window_seconds"]

    path = _get_alert_file(base_dir, org_id, site_id)
    alerts = _load_alerts(path)

    now = datetime.now()

    # -------------------------------------------------
    # CHECK FOR EXISTING ACTIVE ALERT
    # -------------------------------------------------

    for alert in alerts:
        if (
            alert["device_id"] == device_id and
            alert["alert_type"] == alert_type and
            alert["status"] == "ACTIVE"
        ):
            last_seen = _parse_time(alert["last_seen"])
            diff = (now - last_seen).total_seconds()

            if diff <= suppression_window:

                # Flap detected
                alert["flap_count"] += 1
                alert["last_seen"] = _now_str()

                # ---------------------------------------------
                # FLAP FREQUENCY ESCALATION LOGIC
                # ---------------------------------------------

                created_time = _parse_time(alert["created_at"])
                elapsed_seconds = (now - created_time).total_seconds()

                # Prevent division by zero
                elapsed_minutes = max(elapsed_seconds / 60, 1)

                frequency = alert["flap_count"] / elapsed_minutes

                # Escalation policy
                if frequency >= 3:
                    alert["severity"] = "CRITICAL"
                    alert["severity_score"] = SEVERITY_SCORES["CRITICAL"]
                    alert["unstable"] = True
                else:
                    alert["unstable"] = False

                # ---------------------------------------------
                # Run Correlation (with updated flap count)
                # ---------------------------------------------

                correlation = analyze(
                    base_dir,
                    org_id,
                    site_id,
                    device_id,
                    alert_type,
                    alert["created_at"],
                    alert["flap_count"]
                )

                alert["correlation"] = correlation

                # Apply correlation severity override
                override = correlation.get("primary_severity_override")
                if override:
                    alert["severity"] = override
                    alert["severity_score"] = SEVERITY_SCORES.get(override, 1)

                _save_alerts(path, alerts)
                return alert
                
    # -------------------------------------------------
    # CREATE NEW ALERT
    # -------------------------------------------------

    flap_count = 1

    correlation = analyze(
        base_dir,
        org_id,
        site_id,
        device_id,
        alert_type,
        _now_str(),
        flap_count
    )

    severity = base_severity

    override = correlation.get("primary_severity_override")
    if override:
        severity = override

    new_alert = {
        "alert_id": str(uuid.uuid4()),
        "alert_type": alert_type,
        "severity": severity,
        "severity_score": SEVERITY_SCORES.get(severity, 1),

        "org_id": org_id,
        "site_id": site_id,
        "device_id": device_id,

        "created_at": _now_str(),
        "last_seen": _now_str(),
        "resolved_at": "",

        "down_duration_seconds": 0,
        "down_duration_human": "",

        "status": "ACTIVE",
        "flap_count": flap_count,

        "correlation": correlation,

        "acknowledged": False,
        "acknowledged_by": "",
        "acknowledged_at": "",
        
        "unstable": False,

        "suppressed": False
    }

    alerts.append(new_alert)
    _save_alerts(path, alerts)

    return new_alert

# -------------------------------------------------
# Alert Resolution
# -------------------------------------------------

def resolve_alert(
    base_dir,
    org_id,
    site_id,
    device_id,
    alert_type
):

    path = _get_alert_file(base_dir, org_id, site_id)
    alerts = _load_alerts(path)

    now_str = _now_str()
    now = datetime.now()

    for alert in alerts:
        if (
            alert["device_id"] == device_id and
            alert["alert_type"] == alert_type and
            alert["status"] == "ACTIVE"
        ):

            created = _parse_time(alert["created_at"])
            duration_seconds = int((now - created).total_seconds())

            alert["resolved_at"] = now_str
            alert["down_duration_seconds"] = duration_seconds
            alert["down_duration_human"] = _format_duration(duration_seconds)
            alert["status"] = "RESOLVED"

            _save_alerts(path, alerts)
            return alert

    return None


# -------------------------------------------------
# Acknowledgment
# -------------------------------------------------

def acknowledge_alert(
    base_dir,
    org_id,
    site_id,
    alert_id,
    user
):

    path = _get_alert_file(base_dir, org_id, site_id)
    alerts = _load_alerts(path)

    for alert in alerts:
        if alert["alert_id"] == alert_id:
            alert["acknowledged"] = True
            alert["acknowledged_by"] = user
            alert["acknowledged_at"] = _now_str()
            _save_alerts(path, alerts)
            return alert

    return None
