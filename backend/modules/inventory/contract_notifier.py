# backend/modules/inventory/contract_notifier.py

import smtplib
from email.mime.text import MIMEText


SMTP_SERVER = "smtp.yourdomain.com"
SMTP_PORT = 587
SMTP_USERNAME = "alerts@yourdomain.com"
SMTP_PASSWORD = "password"
FROM_EMAIL = "alerts@yourdomain.com"
TO_EMAILS = ["admin@yourdomain.com"]


def send_contract_notifications(result):

    summary = result.get("summary", {})

    if summary.get("expired", 0) == 0 and summary.get("expiring_soon", 0) == 0:
        return  # No alert needed

    subject = f"[ALERT] Contract Expiry Warning - {result['site_id']}"

    body = build_email_body(result)

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = FROM_EMAIL
    msg["To"] = ", ".join(TO_EMAILS)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(FROM_EMAIL, TO_EMAILS, msg.as_string())
    except Exception:
        pass


def build_email_body(result):

    lines = []
    lines.append("Contract Status Report\n")
    lines.append(f"Org: {result['org_id']}")
    lines.append(f"Site: {result['site_id']}\n")

    for device in result["devices"]:
        if device["severity"] in ["CRITICAL", "WARNING"]:
            lines.append(
                f"{device['device_id']} - {device['status']} "
                f"({device['days_remaining']} days)"
            )

    return "\n".join(lines)
