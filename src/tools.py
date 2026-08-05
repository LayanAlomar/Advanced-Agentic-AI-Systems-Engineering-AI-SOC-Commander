from __future__ import annotations
import json
import re
from pathlib import Path
from typing import Any

from .guardrails import validate_action

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def parse_security_logs(text: str) -> dict[str, Any]:
    lower = text.lower()
    failed_logins = len(re.findall(r"failed login|authentication failure", lower))
    suspicious_countries = [c for c in ["russia", "china", "north korea", "iran"] if c in lower]
    outbound_match = re.search(r"(\d+(?:\.\d+)?)\s*(gb|mb)\s+outbound", lower)
    outbound_mb = 0.0
    if outbound_match:
        amount = float(outbound_match.group(1))
        outbound_mb = amount * (1024 if outbound_match.group(2) == "gb" else 1)
    return {
        "failed_login_mentions": failed_logins,
        "suspicious_countries": suspicious_countries,
        "outbound_mb": outbound_mb,
        "contains_phishing_terms": any(x in lower for x in ["phishing", "suspicious email", "malicious link"]),
        "contains_malware_terms": any(x in lower for x in ["malware", "ransomware", "trojan"]),
        "contains_privilege_terms": any(x in lower for x in ["admin account", "privilege escalation", "root access"]),
    }

def lookup_threat_intelligence(indicators: dict[str, Any]) -> dict[str, Any]:
    intel = json.loads((DATA_DIR / "threat_intel.json").read_text(encoding="utf-8"))
    matches = []
    if indicators.get("contains_phishing_terms"):
        matches.append(intel["phishing"])
    if indicators.get("contains_malware_terms"):
        matches.append(intel["malware"])
    if indicators.get("outbound_mb", 0) >= 1024:
        matches.append(intel["data_exfiltration"])
    if indicators.get("failed_login_mentions", 0) > 0 or indicators.get("suspicious_countries"):
        matches.append(intel["credential_attack"])
    return {"matches": matches, "match_count": len(matches)}

def search_security_policy(query: str) -> list[str]:
    paragraphs = (DATA_DIR / "security_policy.txt").read_text(encoding="utf-8").split("\n\n")
    terms = {word.lower() for word in re.findall(r"[A-Za-z]{4,}", query)}
    scored = []
    for paragraph in paragraphs:
        score = sum(term in paragraph.lower() for term in terms)
        if score:
            scored.append((score, paragraph.strip()))
    scored.sort(reverse=True, key=lambda item: item[0])
    return [text for _, text in scored[:4]]

def safe_response_action(action: str, details: str, sensitivity: str) -> dict[str, Any]:
    candidate = {"action": action, "details": details, "sensitivity": sensitivity}
    allowed, reason = validate_action(candidate)
    candidate["allowed"] = allowed
    candidate["validation_reason"] = reason
    return candidate
