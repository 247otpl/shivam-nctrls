# backend/modules/events/correlation/rules.py

RULES = [

    # -----------------------------------------
    # SYSTEM RELOAD
    # -----------------------------------------
    {
        "name": "manual_reload",
        "alert_type": "DEVICE_DOWN",
        "keywords": ["RELOAD", "SYS-5-RELOAD"],
        "probable_cause": "Manual reload detected",
        "confidence": "HIGH",
        "severity_override": "MAJOR",
        "priority": 100
    },

    # -----------------------------------------
    # POWER FAILURE
    # -----------------------------------------
    {
        "name": "power_failure",
        "alert_type": "DEVICE_DOWN",
        "keywords": ["POWER", "PSU", "power supply"],
        "probable_cause": "Power supply failure detected",
        "confidence": "HIGH",
        "severity_override": "CRITICAL",
        "priority": 110
    },

    # -----------------------------------------
    # UPLINK / LINK FAILURE
    # -----------------------------------------
    {
        "name": "uplink_down",
        "alert_type": "DEVICE_DOWN",
        "keywords": ["UPDOWN", "link down", "LINEPROTO"],
        "probable_cause": "Uplink or physical link failure",
        "confidence": "MEDIUM",
        "severity_override": "MAJOR",
        "priority": 70
    },

    # -----------------------------------------
    # STP TOPOLOGY CHANGE
    # -----------------------------------------
    {
        "name": "stp_tcn",
        "alert_type": "DEVICE_DOWN",
        "keywords": ["SPANTREE", "TOPO_CHANGE", "TCN"],
        "probable_cause": "STP topology change detected",
        "confidence": "HIGH",
        "severity_override": "CRITICAL",
        "priority": 120
    },

    # -----------------------------------------
    # AUTHENTICATION FAILURE
    # -----------------------------------------
    {
        "name": "auth_failure",
        "alert_type": "SSH_DOWN",
        "keywords": ["AUTH", "AAA", "authentication failed"],
        "probable_cause": "Authentication or AAA failure",
        "confidence": "MEDIUM",
        "severity_override": "MINOR",
        "priority": 60
    }
]