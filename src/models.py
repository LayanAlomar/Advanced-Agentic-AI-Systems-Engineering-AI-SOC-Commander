from typing import Any, Literal, TypedDict

RiskLevel = Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]

class SOCState(TypedDict, total=False):
    run_id: str
    incident_text: str
    sanitized_input: str
    blocked: bool
    block_reason: str
    plan: list[str]
    indicators: dict[str, Any]
    threat_type: str
    llm_rationale: str
    llm_confidence: float
    llm_trace: dict[str, Any]
    risk_level: RiskLevel
    risk_score: int
    policy_findings: list[str]
    response_plan: list[dict[str, Any]]
    reviewer_feedback: list[str]
    review_passed: bool
    revision_count: int
    requires_approval: bool
    approval_status: str
    final_report: dict[str, Any]
    metrics: dict[str, Any]
    errors: list[str]
