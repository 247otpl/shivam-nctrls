# backend/modules/events/correlation/engine.py

from datetime import datetime
from .rules import RULES
from ..event_store import load_recent_events
from ..settings_service import load_site_settings


CONFIDENCE_SCORE = {
    "LOW": 1,
    "MEDIUM": 2,
    "HIGH": 3
}


def analyze(
    base_dir,
    org_id,
    site_id,
    device_id,
    alert_type,
    alert_timestamp,
    flap_count
):

    settings = load_site_settings(base_dir, org_id, site_id)
    window = settings["correlation_window_seconds"]

    recent_events = load_recent_events(
        base_dir,
        org_id,
        site_id,
        device_id,
        window
    )

    matched = []

    # -------------------------------------------------
    # RULE-BASED MATCHING
    # -------------------------------------------------

    for rule in RULES:

        if rule["alert_type"] != alert_type:
            continue

        for event in recent_events:
            message = event.get("message", "").upper()

            for keyword in rule["keywords"]:
                if keyword.upper() in message:

                    matched.append({
                        "rule": rule,
                        "event": event
                    })
                    break

    # -------------------------------------------------
    # FLAP-BASED STP INFERENCE
    # -------------------------------------------------

    inferred = None

    if alert_type == "DEVICE_DOWN":

        if flap_count >= 3:
            inferred = {
                "probable_cause": "Frequent flapping detected - possible STP instability",
                "confidence": "HIGH",
                "severity_override": "CRITICAL",
                "priority": 115
            }

    # -------------------------------------------------
    # PRIMARY + SECONDARY SELECTION
    # -------------------------------------------------

    candidates = []

    for item in matched:
        rule = item["rule"]
        candidates.append({
            "probable_cause": rule["probable_cause"],
            "confidence": rule["confidence"],
            "severity_override": rule.get("severity_override"),
            "priority": rule.get("priority", 0),
            "related_event": item["event"]
        })

    if inferred:
        candidates.append(inferred)

    if not candidates:
        return {
            "primary_cause": "No related events found",
            "primary_confidence": "LOW",
            "primary_severity_override": None,
            "secondary_causes": [],
            "related_events": [],
            "correlation_window_seconds": window,
            "analyzed_at": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        }

    # Sort by priority first, then confidence
    candidates.sort(
        key=lambda x: (
            x.get("priority", 0),
            CONFIDENCE_SCORE.get(x["confidence"], 0)
        ),
        reverse=True
    )

    primary = candidates[0]
    secondary = candidates[1:]

    return {
        "primary_cause": primary["probable_cause"],
        "primary_confidence": primary["confidence"],
        "primary_severity_override": primary.get("severity_override"),
        "secondary_causes": [
            {
                "cause": s["probable_cause"],
                "confidence": s["confidence"]
            } for s in secondary
        ],
        "related_events": [
            s.get("related_event") for s in candidates
            if s.get("related_event")
        ],
        "correlation_window_seconds": window,
        "analyzed_at": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    }