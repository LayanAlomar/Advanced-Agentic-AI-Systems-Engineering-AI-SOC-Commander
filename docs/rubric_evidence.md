# Rubric Evidence Map — LLM Revision

## Agentic Reasoning & Tool Use
- Gemini `ChatGoogleGenerativeAI` is called in `src/llm_agent.py`.
- Real tools are bound with `bind_tools()`.
- Gemini selects and calls `parse_incident_evidence` and `correlate_threat_intelligence`.
- Tool results are returned through `ToolMessage`.
- A structured `ThreatDecision` contains classification, rationale, confidence, and indicators.

## Graph-Based Orchestration
- Genuine LangGraph `StateGraph`, conditional branches, shared `SOCState`, and bounded reviewer loop.

## Multi-Agent System
- Nine distinct agents coordinated using centralized hierarchical delegation and shared state.

## Security & Observability
- Demonstrated injection blocking, PII masking, unsafe-action and output validation.
- Structured logs capture LLM decisions, tool calls, latency, approval events, and retries.

## Production Readiness
- SQLite checkpointer, real interrupt/resume HITL, FastAPI, Dockerfile, docker-compose.

## Required execution evidence
- Run and save the Colab notebook with outputs.
- Commit generated logs, summary, and screenshots in `evidence/`.
