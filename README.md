<div align="center">

# 🛡️ AI SOC Commander

### Secure Multi-Agent Cybersecurity Incident Response System

**Capstone Project – Advanced Agentic AI Systems Engineering**

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![LangGraph](https://img.shields.io/badge/LangGraph-Agentic_AI-success?style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite)
![Google Colab](https://img.shields.io/badge/Google-Colab-F9AB00?style=flat-square&logo=googlecolab)

Enterprise-grade multi-agent cybersecurity incident response system built with **LangGraph**, **FastAPI**, **SQLite**, **Docker**, and **Google Colab**.

</div>

---

# 📋 Project Information

| Item | Details |
|------|---------|
| **Project** | AI SOC Commander |
| **Program** | Advanced Agentic AI Systems Engineering |
| **Organization** | SDAIA Academy |
| **Trainer** | Eng. Mohammed Albeladi |
| **Architecture** | LangGraph Multi-Agent Workflow |
| **Deployment** | FastAPI + Docker |
| **Persistence** | SQLite Checkpoints |
| **Notebook** | Google Colab |

---

# 📑 Table of Contents

- About
- Key Features
- System Architecture
- Multi-Agent Workflow
- Agent Responsibilities
- Technologies
- Repository Structure
- Installation
- Google Colab Demo
- API Example
- Security Features
- Human-in-the-Loop
- Observability
- Team
- Acknowledgment

---

# 🚀 About

AI SOC Commander is a secure enterprise-style multi-agent cybersecurity incident response system developed as the Capstone Project for the **Advanced Agentic AI Systems Engineering** program.

The system receives cybersecurity incident reports, analyzes threats, evaluates risk levels, retrieves organizational security policies, generates response plans, validates actions using security guardrails, pauses for human approval when required, and produces an auditable incident report.

---

# ✨ Key Features

- Multi-Agent Architecture
- LangGraph StateGraph Orchestration
- Shared Agent State
- Conditional Routing
- Reviewer Feedback Loop
- Human-in-the-Loop Approval
- SQLite Checkpoint Persistence
- Prompt Injection Protection
- PII Masking
- Output Validation
- Structured JSON Logging
- FastAPI REST API
- Docker Deployment
- Google Colab Notebook

---

# 🏗️ System Architecture

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
 │
 ├── Revision Required ───────────┐
 ▼                                │
Human Approval                    │
 │                                │
 ▼                                │
Final Report ◄────────────────────┘
 │
 ▼
Audit Logs
```

---

# 🤖 Multi-Agent Workflow

| Agent | Responsibility |
|------|----------------|
| Input Guardrail | Detects prompt injection and malicious input |
| Coordinator | Controls workflow execution |
| Threat Analyzer | Analyzes cybersecurity incidents |
| Risk Assessment | Determines severity level |
| Policy Agent | Retrieves security policies |
| Response Planner | Builds mitigation strategy |
| Security Reviewer | Reviews response quality |
| Human Approval | Approves sensitive actions |
| Final Report | Produces the final report |

---

# 🛠️ Technologies

- Python
- LangGraph
- FastAPI
- SQLite
- Docker
- Google Colab

---

# 📁 Repository Structure

```text
AI_SOC_Commander/
│
├── AI_SOC_Commander_Colab.ipynb
├── README.md
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── src/
├── data/
├── docs/
└── tests/
```

---

# ▶️ Google Colab Demo

1. Upload the notebook to Google Colab.
2. Click **Runtime → Run All**.
3. Execute all notebook cells.
4. Review generated logs and checkpoints.

---

# 💻 Local Installation

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

---

# 🌐 API Example

```bash
POST /incidents/analyze
```

---

# 🔐 Security Features

- Prompt Injection Detection
- PII Masking
- Safe Action Validation
- Human Approval
- Persistent Checkpoints
- JSON Audit Logs

---

# 👤 Human-in-the-Loop

Sensitive response actions require manual approval before execution continues, ensuring secure decision-making and operational safety.

---

# 📊 Observability

The project records:

- JSONL Audit Logs
- SQLite Checkpoints
- Workflow Events
- Retry Statistics
- Execution Metrics

---

# 👥 Team

| Name | Email |
|------|------|
| Wesal Fadhl Alnoamani | wesalfdhel1957@gmail.com |
| Layan Omar Alomar | layanomaralomar@gmail.com |
| Rawan Hamad Alqahtani | rawan1hamad@hotmail.com |

---

# 🙏 Acknowledgment

This project was developed as the Capstone Project for the **Advanced Agentic AI Systems Engineering** program delivered through **SDAIA Academy**.

Special thanks to **Eng. Mohammed Albeladi** for his guidance and support throughout the program.

GitHub:
https://github.com/SDAIAAcademy

---

<div align="center">

**AI SOC Commander © 2026**

Built for the Advanced Agentic AI Systems Engineering Program

</div>