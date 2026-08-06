from __future__ import annotations
from typing import Any

from .guardrails import detect_prompt_injection, mask_pii, validate_report
from .observability import log_event, timed
from .tools import parse_security_logs, lookup_threat_intelligence, search_security_policy, safe_response_action

def _metrics(state: dict[str, Any]) -> dict[str, Any]:
    return dict(state.get("metrics", {"tool_calls": 0, "failures": 0, "retries": 0, "blocked_attacks": 0, "approval_pauses": 0, "latency_ms": 0.0}))

def input_guardrail_agent(state: dict[str, Any]) -> dict[str, Any]:
    run_id = state["run_id"]
    blocked, reason = detect_prompt_injection(state["incident_text"])
    metrics = _metrics(state)
    if blocked:
        metrics["blocked_attacks"] += 1
        log_event(run_id, "input_guardrail", "attack_blocked", reason=reason)
        return {"blocked": True, "block_reason": reason, "metrics": metrics}
    sanitized = mask_pii(state["incident_text"])
    log_event(run_id, "input_guardrail", "input_allowed")
    return {"blocked": False, "sanitized_input": sanitized, "metrics": metrics}

def coordinator_agent(state: dict[str, Any]) -> dict[str, Any]:
    plan = [
        "Parse incident evidence with the log-analysis tool",
        "Correlate evidence with local threat intelligence",
        "Calculate business risk",
        "Retrieve relevant security policies",
        "Create a bounded and reversible response plan",
        "Review the plan and revise when necessary",
        "Request human approval for sensitive actions",
        "Generate a PII-safe final report",
    ]
    log_event(state["run_id"], "coordinator", "plan_created", steps=len(plan), reasoning_pattern="Plan-and-Execute")
    return {"plan": plan}

def threat_analyzer_agent(state: dict[str, Any]) -> dict[str, Any]:
    """Real LLM decision point using Gemini function calling."""
    from .llm_agent import classify_threat_with_function_calling

    run_id = state["run_id"]
    metrics = _metrics(state)
    decision, llm_metadata = classify_threat_with_function_calling(state["sanitized_input"], run_id)
    metrics["tool_calls"] += len(llm_metadata["tool_trace"])
    metrics["llm_calls"] = metrics.get("llm_calls", 0) + llm_metadata["llm_calls"]
    metrics["latency_ms"] += llm_metadata["latency_ms"]
    return {
        "indicators": decision.indicators,
        "threat_type": decision.threat_type,
        "llm_rationale": decision.rationale,
        "llm_confidence": decision.confidence,
        "llm_trace": llm_metadata,
        "metrics": metrics,
    }

def risk_assessment_agent(state: dict[str, Any]) -> dict[str, Any]:
    indicators = state["indicators"]
    score = 10
    score += min(indicators.get("failed_login_mentions", 0) * 10, 20)
    score += 20 if indicators.get("suspicious_countries") else 0
    score += 30 if indicators.get("outbound_mb", 0) >= 1024 else 0
    score += 25 if indicators.get("contains_malware_terms") else 0
    score += 15 if indicators.get("contains_privilege_terms") else 0
    score = min(score, 100)

    if score >= 80:
        level = "CRITICAL"
    elif score >= 60:
        level = "HIGH"
    elif score >= 35:
        level = "MEDIUM"
    else:
        level = "LOW"

    log_event(state["run_id"], "risk_assessor", "risk_scored", score=score, level=level)
    return {"risk_score": score, "risk_level": level}

def policy_agent(state: dict[str, Any]) -> dict[str, Any]:
    metrics = _metrics(state)
    query = f"{state['threat_type']} {state['risk_level']} isolation account evidence approval"
    findings, latency = timed(state["run_id"], "policy_agent.search_security_policy", search_security_policy, query)
    metrics["tool_calls"] += 1
    metrics["latency_ms"] += latency
    log_event(state["run_id"], "policy_agent", "policy_retrieved", findings=len(findings))
    return {"policy_findings": findings, "metrics": metrics}

def response_planner_agent(state: dict[str, Any]) -> dict[str, Any]:
    risk = state["risk_level"]
    threat = state["threat_type"]
    actions = [
        safe_response_action("Preserve evidence", "Create a read-only evidence snapshot and retain relevant logs.", "LOW"),
        safe_response_action("Increase monitoring", "Enable enhanced authentication, endpoint, and egress monitoring for affected assets.", "LOW"),
    ]

    if threat in {"Credential Attack", "Phishing / Credential Theft"}:
        actions.append(safe_response_action("Reset affected credentials", "Force password reset and revoke active sessions for specifically identified accounts.", "HIGH"))
    if threat in {"Potential Data Exfiltration", "Malware Infection"}:
        actions.append(safe_response_action("Isolate affected endpoint", "Quarantine only the confirmed endpoint from the production network while preserving forensic access.", "HIGH"))
    if risk in {"HIGH", "CRITICAL"}:
        actions.append(safe_response_action("Notify incident commander", "Escalate to the designated SOC incident commander and legal/privacy contacts when required.", "MEDIUM"))

    feedback = state.get("reviewer_feedback", [])
    if feedback:
        actions.append(safe_response_action("Address reviewer feedback", "; ".join(feedback), "LOW"))

    actions = [a for a in actions if a["allowed"]]
    requires_approval = any(a["sensitivity"] == "HIGH" for a in actions)
    log_event(state["run_id"], "response_planner", "plan_created", actions=len(actions), requires_approval=requires_approval)
    return {"response_plan": actions, "requires_approval": requires_approval}

def reviewer_agent(state: dict[str, Any]) -> dict[str, Any]:
    feedback = []
    actions = state.get("response_plan", [])
    revision_count = state.get("revision_count", 0)

    if not any(a["action"] == "Preserve evidence" for a in actions):
        feedback.append("Add evidence preservation before containment.")
    if state["risk_level"] in {"HIGH", "CRITICAL"} and not any("Notify incident commander" == a["action"] for a in actions):
        feedback.append("Escalate high-risk incidents to the incident commander.")
    if revision_count == 0 and state["risk_level"] == "CRITICAL":
        feedback.append("Add a communication and stakeholder-notification step for the critical incident.")

    passed = len(feedback) == 0 or revision_count >= 1
    next_revision = revision_count + (0 if passed else 1)
    metrics = _metrics(state)
    if not passed:
        metrics["retries"] += 1
    log_event(state["run_id"], "security_reviewer", "review_complete", passed=passed, feedback=feedback, revision_count=next_revision)
    return {
        "reviewer_feedback": feedback,
        "review_passed": passed,
        "revision_count": next_revision,
        "metrics": metrics,
    }

def rejected_plan_agent(state: dict[str, Any]) -> dict[str, Any]:
    safe_plan = [
        safe_response_action("Preserve evidence", "Keep existing evidence in read-only storage.", "LOW"),
        safe_response_action("Monitor and escalate", "Continue monitoring and send the case to the incident commander for manual handling.", "LOW"),
    ]
    log_event(state["run_id"], "rejected_plan", "human_rejected_sensitive_actions")
    return {"response_plan": safe_plan, "approval_status": "REJECTED - SAFE ALTERNATIVE USED"}

def final_report_agent(state: dict[str, Any]) -> dict[str, Any]:
    report = {
        "incident_summary": mask_pii(state.get("sanitized_input", state.get("incident_text", ""))),
        "threat_type": state.get("threat_type", "Not analyzed"),
        "risk_level": state.get("risk_level", "LOW"),
        "risk_score": state.get("risk_score", 0),
        "evidence": state.get("indicators", {}),
        "llm_reasoning": {
            "rationale": state.get("llm_rationale", ""),
            "confidence": state.get("llm_confidence", 0.0),
            "model": state.get("llm_trace", {}).get("model", ""),
            "tool_calls": state.get("llm_trace", {}).get("tool_trace", []),
        },
        "policy_findings": [mask_pii(x) for x in state.get("policy_findings", [])],
        "recommended_actions": state.get("response_plan", []),
        "approval_status": state.get("approval_status", "NOT REQUIRED"),
        "review_feedback": state.get("reviewer_feedback", []),
        "revision_count": state.get("revision_count", 0),
        "reasoning_pattern": "Plan-and-Execute with reviewer self-critique",
        "coordination_strategy": "Centralized hierarchical delegation",
    }
    report = validate_report(report)
    log_event(state["run_id"], "final_report", "report_generated", risk_level=report["risk_level"])
    return {"final_report": report}
