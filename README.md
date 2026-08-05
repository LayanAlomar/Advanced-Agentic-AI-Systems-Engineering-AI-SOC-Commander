🛡️ AI SOC Commander

Secure Multi-Agent Cybersecurity Incident Response System

Capstone Project — Advanced Agentic AI Systems Engineering

Built with LangGraph • FastAPI • SQLite • Docker • Google Colab

────────

📑 Table of Contents

• About
• Features
• Architecture
• Multi-Agent Workflow
• Technologies
• Repository Structure
• Google Colab
• Local Setup
• API Example
• Security Features
• Human-in-the-Loop
• Observability
• Team
• Acknowledgment

────────

🚀 About

AI SOC Commander is an enterprise-style multi-agent cybersecurity incident response system developed as the capstone project for the Advanced Agentic AI Systems Engineering program.

Trainer: Eng. Mohammed Albladi

SDAIA Academy: https://github.com/SDAIAAcademy

────────

✨ Features

• LangGraph StateGraph
• Multi-Agent Workflow
• Shared State
• Conditional Routing
• Reviewer Retry Loop
• Human-in-the-Loop
• SQLite Persistence
• Prompt Injection Protection
• PII Masking
• Output Validation
• JSON Audit Logs
• FastAPI
• Docker
• Google Colab

────────

🏗️ Architecture

User → Guardrail → Coordinator → Threat Analyzer → Risk Assessment → Policy Agent → Response Planner → Security Reviewer → Human Approval → Final Report

────────

🤖 Multi-Agent Workflow

• Input Guardrail
• Coordinator
• Threat Analyzer
• Risk Assessment
• Policy Agent
• Response Planner
• Security Reviewer
• Human Approval
• Final Report

────────

🛠️ Technologies

• Python
• LangGraph
• FastAPI
• SQLite
• Docker
• Google Colab

────────

📁 Repository Structure

```text
AI_SOC_Commander/
├── AI_SOC_Commander_Colab.ipynb
├── README.md
├── app.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── src/
├── docs/
├── tests/
└── data/
```

────────

▶️ Google Colab

Run Runtime → Run all then review outputs and download:

• soc_events.jsonl
• soc_checkpoints.sqlite

────────

💻 Local Setup

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

────────

🌐 API Example

```bash
curl -X POST http://127.0.0.1:8000/incidents/analyze
```

────────

🔐 Security Features

• Prompt Injection Detection
• PII Masking
• Output Validation
• Human Approval
• Structured Logging

────────

📊 Observability

• JSONL Audit Logs
• SQLite Checkpoints
• Execution Metrics

────────

👥 Team

|Name                 |Email                    |
|---------------------|-------------------------|
|Wesal Fadhl Alnoamani|wesalfdhel1957@gmail.com |
|Layan Omar Alomar    |layanomaralomar@gmail.com|
|Rawan Hamad Alqahtani|rawan1hamad@hotmail.com  |

────────

🙏 Acknowledgment

Developed as the Capstone Project for the Advanced Agentic AI Systems Engineering program delivered through SDAIA Academy.

Special thanks to Eng. Mohammed Albladi.