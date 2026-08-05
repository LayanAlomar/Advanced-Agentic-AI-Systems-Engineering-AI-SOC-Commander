# Rubric Evidence Map

## 1. Agentic Reasoning & Tool Use — 15 points
- Explicit pattern: Plan-and-Execute.
- Short-term memory: `SOCState`.
- Real tools:
  - `parse_security_logs`
  - `lookup_threat_intelligence`
  - `search_security_policy`
  - `safe_response_action`
- Evidence cells in the Colab notebook show tool outputs.

## 2. Graph-Based Orchestration — 20 points
- Framework: LangGraph `StateGraph`.
- Conditional edges:
  - input allowed vs blocked,
  - reviewer pass vs revision,
  - approval vs rejection.
- Loop:
  - `security_reviewer -> response_planner`.
- Termination:
  - reviewer passes or bounded revision count is reached.

## 3. Multi-Agent System — 20 points
Agents:
1. Input Guardrail Agent
2. Coordinator Agent
3. Threat Analyzer Agent
4. Risk Assessment Agent
5. Policy Agent
6. Response Planner Agent
7. Security Reviewer Agent
8. Human Approval Agent
9. Final Report Agent

Coordination: centralized hierarchical delegation through shared state.

## 4. Security, Guardrails & Observability — 20 points
- Prompt-injection attack is actually blocked.
- PII masking is actually demonstrated.
- Destructive actions are validated and blocked.
- Structured JSONL monitoring captures node, event, latency, failure, and run ID.
- Metrics capture tool calls, retries, blocked attacks, approval pauses, and latency.

## 5. Production Readiness — 20 points
- Persistent SQLite checkpointer.
- Real LangGraph interrupt and resume using `interrupt()` and `Command(resume=...)`.
- FastAPI endpoint.
- Dockerfile and docker-compose.
- Restart-surviving state stored in SQLite.

## 6. Documentation & Execution Evidence — 5 points
- Professional README.
- Architecture diagram.
- Executed demonstration cells should be preserved after running in Colab.
- Repository attribution to SDAIA Academy and trainer.
