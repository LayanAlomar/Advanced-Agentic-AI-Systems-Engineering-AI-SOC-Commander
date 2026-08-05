from __future__ import annotations
from fastapi import FastAPI
from pydantic import BaseModel, Field

from src.graph import Command, build_graph, new_input

app = FastAPI(
    title="AI SOC Commander API",
    version="1.0.0",
    description="Secure multi-agent cybersecurity incident response service.",
)
graph = build_graph()

class IncidentRequest(BaseModel):
    incident_text: str = Field(min_length=5)
    thread_id: str = "api-demo"
    auto_approve: bool = False

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}

@app.post("/incidents/analyze")
def analyze(request: IncidentRequest) -> dict:
    config = {"configurable": {"thread_id": request.thread_id}}
    result = graph.invoke(new_input(request.incident_text), config=config)

    if "__interrupt__" in result:
        if request.auto_approve:
            result = graph.invoke(Command(resume={"approved": True, "approver": "API auto-approval demo"}), config=config)
        else:
            return {
                "status": "approval_required",
                "thread_id": request.thread_id,
                "interrupt": result["__interrupt__"],
            }
    return {"status": "completed", "thread_id": request.thread_id, "result": result}

class ApprovalRequest(BaseModel):
    thread_id: str
    approved: bool
    approver: str = "Human SOC Analyst"

@app.post("/incidents/approve")
def approve(request: ApprovalRequest) -> dict:
    config = {"configurable": {"thread_id": request.thread_id}}
    result = graph.invoke(
        Command(resume={"approved": request.approved, "approver": request.approver}),
        config=config,
    )
    return {"status": "completed", "thread_id": request.thread_id, "result": result}
