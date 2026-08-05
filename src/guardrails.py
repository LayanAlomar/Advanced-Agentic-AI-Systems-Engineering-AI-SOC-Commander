from __future__ import annotations
import re
from typing import Any

INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"reveal\s+(the\s+)?system\s+prompt",
    r"developer\s+message",
    r"bypass\s+(the\s+)?guardrails",
    r"act\s+as\s+an?\s+unrestricted",
    r"jailbreak",
]

UNSAFE_ACTION_PATTERNS = [
    r"delete\s+all",
    r"drop\s+database",
    r"rm\s+-rf",
    r"wipe\s+(all\s+)?servers",
    r"disable\s+all\s+accounts",
]

def detect_prompt_injection(text: str) -> tuple[bool, str]:
    normalized = text.lower()
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, normalized, flags=re.I):
            return True, f"Prompt-injection pattern detected: {pattern}"
    return False, ""

def mask_pii(text: str) -> str:
    text = re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", "[REDACTED_EMAIL]", text)
    text = re.sub(r"(?<!\d)(?:\+?966|0)?5\d{8}(?!\d)", "[REDACTED_PHONE]", text)
    text = re.sub(r"(?<!\d)[12]\d{9}(?!\d)", "[REDACTED_NATIONAL_ID]", text)
    text = re.sub(r"\b(?:\d[ -]*?){13,19}\b", "[REDACTED_PAYMENT_CARD]", text)
    return text

def validate_action(action: dict[str, Any]) -> tuple[bool, str]:
    combined = f"{action.get('action', '')} {action.get('details', '')}".lower()
    for pattern in UNSAFE_ACTION_PATTERNS:
        if re.search(pattern, combined, flags=re.I):
            return False, f"Unsafe or overly broad action blocked: {pattern}"
    return True, ""

def validate_report(report: dict[str, Any]) -> dict[str, Any]:
    required = {"incident_summary", "threat_type", "risk_level", "recommended_actions", "approval_status"}
    missing = sorted(required - set(report))
    if missing:
        raise ValueError(f"Output validation failed. Missing fields: {missing}")
    return report
