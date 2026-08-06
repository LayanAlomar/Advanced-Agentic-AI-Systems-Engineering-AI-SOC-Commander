from __future__ import annotations

import json
import os
import time
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

from .config import settings
from .observability import log_event
from .tools import parse_security_logs, lookup_threat_intelligence


class ThreatDecision(BaseModel):
    threat_type: str = Field(description="Concise cybersecurity incident classification")
    rationale: str = Field(description="Evidence-grounded explanation")
    confidence: float = Field(ge=0.0, le=1.0)
    indicators: dict[str, Any]


@tool
def parse_incident_evidence(incident_text: str) -> dict[str, Any]:
    """Parse a cybersecurity incident report into objective indicators."""
    return parse_security_logs(incident_text)


@tool
def correlate_threat_intelligence(indicators_json: str) -> dict[str, Any]:
    """Correlate parsed incident indicators with the local threat-intelligence catalogue."""
    indicators = json.loads(indicators_json)
    return lookup_threat_intelligence(indicators)


TOOLS = [parse_incident_evidence, correlate_threat_intelligence]
TOOL_MAP = {tool.name: tool for tool in TOOLS}


def _model() -> ChatGoogleGenerativeAI:
    if not os.getenv("GOOGLE_API_KEY"):
        raise RuntimeError(
            "GOOGLE_API_KEY is required. In Colab, enter it in the API-key setup cell before running the LLM workflow."
        )
    return ChatGoogleGenerativeAI(model=settings.gemini_model, temperature=0)


def classify_threat_with_function_calling(incident_text: str, run_id: str) -> tuple[ThreatDecision, dict[str, Any]]:
    """Use Gemini tool calling to choose and execute real analysis tools, then classify the incident."""
    llm = _model()
    tool_llm = llm.bind_tools(TOOLS)
    messages = [
        SystemMessage(content=(
            "You are the Threat Analyzer Agent in a defensive SOC. Use the available tools to inspect the incident. "
            "You must call parse_incident_evidence first. Then call correlate_threat_intelligence using the parsed "
            "indicators serialized as JSON. Do not invent evidence. After tools return, explain the likely threat."
        )),
        HumanMessage(content=incident_text),
    ]

    tool_trace: list[dict[str, Any]] = []
    total_latency_ms = 0.0
    for _ in range(4):
        started = time.perf_counter()
        response = tool_llm.invoke(messages)
        total_latency_ms += (time.perf_counter() - started) * 1000
        messages.append(response)
        if not response.tool_calls:
            break
        for call in response.tool_calls:
            name = call["name"]
            args = call.get("args", {})
            if name not in TOOL_MAP:
                raise ValueError(f"Model requested unknown tool: {name}")
            started_tool = time.perf_counter()
            result = TOOL_MAP[name].invoke(args)
            tool_latency = round((time.perf_counter() - started_tool) * 1000, 2)
            tool_trace.append({"tool": name, "args": args, "result": result, "latency_ms": tool_latency})
            log_event(run_id, "llm_threat_analyzer", "llm_tool_call", tool=name, latency_ms=tool_latency)
            messages.append(ToolMessage(content=json.dumps(result), tool_call_id=call["id"]))
    else:
        raise RuntimeError("LLM tool-calling loop exceeded the maximum number of iterations")

    parsed = next((x["result"] for x in tool_trace if x["tool"] == "parse_incident_evidence"), {})
    intel = next((x["result"] for x in tool_trace if x["tool"] == "correlate_threat_intelligence"), {})
    if not parsed:
        raise RuntimeError("The LLM did not call the required parse_incident_evidence tool")

    structured_llm = llm.with_structured_output(ThreatDecision)
    synthesis_prompt = (
        "Classify this cybersecurity incident using only the supplied incident, parsed indicators, and threat intelligence. "
        "Return an evidence-grounded ThreatDecision.\n\n"
        f"INCIDENT:\n{incident_text}\n\nPARSED INDICATORS:\n{json.dumps(parsed)}\n\n"
        f"THREAT INTELLIGENCE:\n{json.dumps(intel)}"
    )
    started = time.perf_counter()
    decision = structured_llm.invoke(synthesis_prompt)
    total_latency_ms += (time.perf_counter() - started) * 1000
    decision.indicators["threat_intelligence"] = intel
    metadata = {
        "model": settings.gemini_model,
        "tool_trace": tool_trace,
        "llm_calls": 1 + sum(1 for _ in tool_trace) + 1,
        "latency_ms": round(total_latency_ms, 2),
    }
    log_event(
        run_id,
        "llm_threat_analyzer",
        "llm_decision_complete",
        model=settings.gemini_model,
        threat_type=decision.threat_type,
        confidence=decision.confidence,
        tool_calls=len(tool_trace),
        latency_ms=metadata["latency_ms"],
    )
    return decision, metadata
