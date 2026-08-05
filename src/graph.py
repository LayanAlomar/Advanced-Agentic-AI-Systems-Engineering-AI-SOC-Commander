from __future__ import annotations
import sqlite3
import uuid
from typing import Any

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt

from .agents import (
    coordinator_agent,
    final_report_agent,
    input_guardrail_agent,
    policy_agent,
    rejected_plan_agent,
    response_planner_agent,
    reviewer_agent,
    risk_assessment_agent,
    threat_analyzer_agent,
)
from .config import settings
from .models import SOCState
from .observability import log_event

def approval_agent(state: SOCState) -> dict[str, Any]:
    metrics = dict(state.get("metrics", {}))
    metrics["approval_pauses"] = metrics.get("approval_pauses", 0) + 1
    log_event(state["run_id"], "human_approval", "paused_for_approval", actions=state.get("response_plan", []))
    decision = interrupt({
        "message": "Sensitive containment action requires human approval.",
        "risk_level": state["risk_level"],
        "proposed_actions": state["response_plan"],
    })
    approved = bool(decision.get("approved")) if isinstance(decision, dict) else bool(decision)
    status = "APPROVED" if approved else "REJECTED"
    log_event(state["run_id"], "human_approval", "resumed", approval_status=status)
    return {"approval_status": status, "metrics": metrics}

def route_after_guardrail(state: SOCState) -> str:
    return "blocked_final" if state.get("blocked") else "coordinator"

def blocked_final(state: SOCState) -> dict[str, Any]:
    return {
        "final_report": {
            "incident_summary": "Request blocked by the input security guardrail.",
            "threat_type": "Prompt Injection Attempt",
            "risk_level": "HIGH",
            "recommended_actions": [{"action": "Reject request", "details": state.get("block_reason", ""), "sensitivity": "LOW"}],
            "approval_status": "BLOCKED",
        }
    }

def route_after_review(state: SOCState) -> str:
    if not state.get("review_passed", False) and state.get("revision_count", 0) < 2:
        return "response_planner"
    if state.get("requires_approval", False):
        return "human_approval"
    return "final_report"

def route_after_approval(state: SOCState) -> str:
    return "final_report" if state.get("approval_status") == "APPROVED" else "rejected_plan"

def build_graph(db_path: str | None = None):
    builder = StateGraph(SOCState)
    builder.add_node("input_guardrail", input_guardrail_agent)
    builder.add_node("blocked_final", blocked_final)
    builder.add_node("coordinator", coordinator_agent)
    builder.add_node("threat_analyzer", threat_analyzer_agent)
    builder.add_node("risk_assessor", risk_assessment_agent)
    builder.add_node("policy_agent", policy_agent)
    builder.add_node("response_planner", response_planner_agent)
    builder.add_node("security_reviewer", reviewer_agent)
    builder.add_node("human_approval", approval_agent)
    builder.add_node("rejected_plan", rejected_plan_agent)
    builder.add_node("final_report", final_report_agent)

    builder.add_edge(START, "input_guardrail")
    builder.add_conditional_edges("input_guardrail", route_after_guardrail, {
        "blocked_final": "blocked_final",
        "coordinator": "coordinator",
    })
    builder.add_edge("blocked_final", END)
    builder.add_edge("coordinator", "threat_analyzer")
    builder.add_edge("threat_analyzer", "risk_assessor")
    builder.add_edge("risk_assessor", "policy_agent")
    builder.add_edge("policy_agent", "response_planner")
    builder.add_edge("response_planner", "security_reviewer")
    builder.add_conditional_edges("security_reviewer", route_after_review, {
        "response_planner": "response_planner",
        "human_approval": "human_approval",
        "final_report": "final_report",
    })
    builder.add_conditional_edges("human_approval", route_after_approval, {
        "final_report": "final_report",
        "rejected_plan": "rejected_plan",
    })
    builder.add_edge("rejected_plan", "final_report")
    builder.add_edge("final_report", END)

    connection = sqlite3.connect(db_path or settings.checkpoint_db, check_same_thread=False)
    checkpointer = SqliteSaver(connection)
    return builder.compile(checkpointer=checkpointer)

def new_input(incident_text: str) -> SOCState:
    return {
        "run_id": str(uuid.uuid4()),
        "incident_text": incident_text,
        "metrics": {
            "tool_calls": 0,
            "failures": 0,
            "retries": 0,
            "blocked_attacks": 0,
            "approval_pauses": 0,
            "latency_ms": 0.0,
        },
        "revision_count": 0,
        "errors": [],
    }

__all__ = ["build_graph", "new_input", "Command"]
