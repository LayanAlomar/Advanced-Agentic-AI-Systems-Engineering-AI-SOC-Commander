<div align="center">

🛡️ AI SOC Commander

Secure Multi-Agent Cybersecurity Incident Response System

Capstone Project — Advanced Agentic AI Systems Engineering

Python
LangGraph
FastAPI
Docker
SQLite
Google Colab

Enterprise-style Multi-Agent SOC workflow built with LangGraph, FastAPI, SQLite, Docker, and Google Colab.

</div>

────────

📑 Table of Contents

• About
• Key Features
• Architecture
• Multi-Agent Workflow
• Agent Responsibilities
• Technologies
• Repository Structure
• Google Colab Demo
• Local Setup
• API Example
• Security Features
• Human-in-the-Loop
• Observability
• Team
• Acknowledgment

────────

🚀 About

AI SOC Commander is a secure enterprise-style multi-agent cybersecurity incident response system developed as the Capstone Project for the Advanced Agentic AI Systems Engineering program.

The workflow analyzes incidents, evaluates risk, retrieves organizational security policies, generates response plans, applies security guardrails, requests human approval for sensitive actions, and produces an auditable security report.

Program: Advanced Agentic AI Systems Engineering

Delivered by: SDAIA Academy

Trainer: Eng. Mohammed Albladi

SDAIA Academy GitHub:
https://github.com/SDAIAAcademy

────────

✨ Key Features

• LangGraph StateGraph orchestration
• Multi-Agent architecture
• Shared workflow state
• Conditional routing
• Reviewer retry loop
• Human-in-the-loop approval
• SQLite checkpoint persistence
• Prompt Injection protection
• PII masking
• Output validation
• JSONL audit logs
• FastAPI REST API
• Docker deployment
• Google Colab notebook

────────

🏗️ Architecture

```text
User
 │
 ▼
Input Guardrail
 │
 ▼
Coordinator
 │
 ▼
Threat Analyzer
 │
 ▼
Risk Assessment
 │
 ▼
Policy Agent
 │
 ▼
Response Planner
 │
 ▼
Security Reviewer
 ├──── Revision Required ───► Planner
 │
 ▼
Human Approval
 │
 ▼
Final Report
 │
 ▼
Audit Logs
```

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

👨‍💻 Agent Responsibilities

|Agent            |Responsibility                |
|-----------------|------------------------------|
|Input Guardrail  |Blocks malicious prompts      |
|Coordinator      |Manages workflow              |
|Threat Analyzer  |Parses security incidents     |
|Risk Assessment  |Calculates severity           |
|Policy Agent     |Retrieves security policies   |
|Response Planner |Creates response plan         |
|Security Reviewer|Reviews and requests revisions|
|Human Approval   |Approves sensitive actions    |
|Final Report     |Generates incident report     |

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
├── data/
└── tests/
```

────────

▶️ Google Colab Demo

1. Open the notebook.
2. Runtime → Run all.
3. Execute every cell.
4. Download:
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
• Safe Response Planning
• Human Approval
• Persistent Execution State

────────

👤 Human-in-the-Loop

Sensitive actions pause execution until approval or rejection is received before the workflow resumes.

────────

📊 Observability

• JSONL Audit Logs
• SQLite Checkpoints
• Tool Calls
• Retry Count
• Approval Pauses
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

Special thanks to Eng. Mohammed Albeladi for his guidance and support throughout the program.