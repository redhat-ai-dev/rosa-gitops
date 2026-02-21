import logging
import os

import requests
from flask import Flask, request, jsonify

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SLACK_WEBHOOK_URL = os.environ["SLACK_WEBHOOK_URL"]


def build_message(alert, status):
    alertname = alert.get("labels", {}).get("alertname", "unknown")
    severity = alert.get("labels", {}).get("severity", "unknown")
    namespace = alert.get("labels", {}).get("namespace", "unknown")
    pod = alert.get("labels", {}).get("pod", "")
    summary = alert.get("annotations", {}).get("summary", "")
    description = alert.get("annotations", {}).get("description", "")

    if status == "firing":
        title = f"[FIRING] {alertname}"
        emoji = "\U0001f534"  # red circle
    else:
        title = f"[RESOLVED] {alertname}"
        emoji = "\u2705"  # check mark

    severity_emoji = "\U0001f525" if severity == "critical" else "\u26a0\ufe0f"

    lines = [
        f"{emoji} {title}",
        "",
        f"Severity: {severity_emoji} {severity}",
        f"Namespace: {namespace}",
    ]
    if pod:
        lines.append(f"Pod: {pod}")
    lines.append("")
    lines.append(f"Summary: {summary}")
    lines.append(f"Description: {description}")

    return title, "\n".join(lines)


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "invalid JSON"}), 400

    status = data.get("status", "unknown")
    alerts = data.get("alerts", [])
    if not alerts:
        return jsonify({"error": "no alerts"}), 400

    for alert in alerts:
        alert_status = alert.get("status", status)
        title, text = build_message(alert, alert_status)

        try:
            resp = requests.post(
                SLACK_WEBHOOK_URL,
                json={"title": title, "text": text},
                timeout=10,
            )
            logger.info(
                "Forwarded alert=%s status=%s slack_status=%d",
                alert.get("labels", {}).get("alertname"),
                alert_status,
                resp.status_code,
            )
        except requests.RequestException:
            logger.exception("Failed to forward alert to Slack")

    return jsonify({"status": "ok"}), 200


@app.route("/healthz", methods=["GET"])
def healthz():
    return jsonify({"status": "ok"}), 200
