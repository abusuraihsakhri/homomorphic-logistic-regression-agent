# Homomorphic Logistic Regression Agent

> **Domain:** Post-Quantum Cryptography & Zero-Knowledge Architecture
> **Reference Guidelines & Standards:** `NIST FIPS 203/204/205, NIST SP 800-90B & ISO/IEC Standards`

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB.svg?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688.svg?logo=fastapi&logoColor=white)
![Audit Trail](https://img.shields.io/badge/Audit-HMAC--SHA256_Tamper--Evident-brightgreen.svg)
![Zero-PHI Guard](https://img.shields.io/badge/Guard-Zero--PHI_Outbound-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)

</div>

---

## 📖 What It Does

**Homomorphic Logistic Regression Agent** is an advanced analytical and computational platform implementing Encrypted gradient descent using Taylor series sigmoid approximations for clinical risk. It provides a multi-worker evaluation system that processes task payloads through specialized workers to produce consensus dossiers with cryptographic audit trails.

---

## ⚙️ Key Capabilities & Algorithmic Modules

- **Deterministic Calculation Engine**: Strict compliance with standard reference formulations and thresholds.
- **Risk & Urgency Classification**: Multi-tier categorization with automated clinical/operational action recommendations.
- **Validation & Guardrails**: Rigorous input bounds checking and anomaly detection.
- **Multi-Worker Evaluation**: Three specialized workers (InvariantQC, SafetyEscalation, ProtocolConformance) analyze each task.
- **Enrichment Suite**: Eight feature engines for comprehensive domain analysis.

---

## 💻 Installation

```bash
# Clone the repository
git clone https://github.com/abusuraihsakhri/homomorphic-logistic-regression-agent.git
cd homomorphic-logistic-regression-agent

# Install dependencies
pip install fastapi uvicorn pydantic pytest

# Optional: Set audit secret key for persistent audit trails
export AUDIT_SECRET_KEY="your-secure-key-here"
```

---

## 💻 CLI Quickstart & Usage

### 1. Single Task Evaluation
```bash
python cli.py audit --task-id TASK-001 --target TARGET-01 --primary 28.5 --secondary 14.2 --critical --status DISCORDANT
```

### 2. Interactive Chat
```bash
python cli.py chat "What is the system status?"
```

### 3. Batch Processing
```bash
python cli.py batch -i sample.csv -o results.csv
```

### 4. Verify Audit Trail Integrity
```bash
python cli.py verify-audit
```

### 5. Launch REST API Server
```bash
python cli.py serve --host 127.0.0.1 --port 8000
```

### Parameter Reference
- `--task-id`: Unique task/case identifier (required, non-empty)
- `--target`: Target entity identifier (required, non-empty)
- `--primary`: Primary metric value (required, finite number)
- `--secondary`: Secondary metric value (default: 0.0, finite number)
- `--critical`: Flag for critical/emergency escalation
- `--status`: Status descriptor (default: NOMINAL)

### Input Data Schema

| Field | Description | Requirement |
|:------|:------------|:------------|
| `task_id` | Parameter / observation metric | Required, non-empty |
| `target_identifier` | Parameter / observation metric | Required, non-empty |
| `primary_metric` | Primary measurement value | Required, finite number |
| `secondary_metric` | Secondary measurement value | Optional, finite number |
| `is_critical_flag` | Emergency escalation flag | Optional, boolean |
| `status_descriptor` | Status code descriptor | Optional, non-empty |

---

## 🔒 REST API Endpoints

| Method | Endpoint | Description |
|:-------|:---------|:------------|
| GET | `/health` | Health check and system metadata |
| GET | `/metrics` | Operational metrics |
| POST | `/api/audit` | Submit task for evaluation |
| POST | `/api/chat` | Query supervisory chat |
| GET | `/api/audit/logs` | Retrieve HMAC-verified audit trail |

---

## 🛡️ Security & Enterprise Architecture

* **Zero-PHI Outbound Interceptor:** Active regex inspection blocking SSNs, MRNs, phone numbers, and patient identifiers.
* **Tamper-Evident HMAC-SHA256 Audit Trail:** Chained, cryptographically signed logs for every evaluation and state transition.
* **Input Validation:** All metric values validated as finite numbers; string identifiers checked for non-empty values.
* **Batch Error Handling:** Invalid rows are skipped and reported without halting processing.
* **Air-Gapped LLM Reasoning Adapter:** Agnostic integration for local Ollama instances (`llama3`, `mistral`), Claude 3.5 Sonnet, GPT-4o, and deterministic test mocks.

---

## 🧪 Testing & Verification

Run the automated test suite:

```bash
pytest -v
```

Execute high-throughput batch simulation benchmarks:

```bash
python simulator.py 1000
```

---

## 🐳 Container Deployment

```bash
docker build -t homomorphic-logistic-regression-agent .
docker run -p 8000:8000 -e AUDIT_SECRET_KEY=your-secure-key homomorphic-logistic-regression-agent
```

Or using Docker Compose:

```bash
docker-compose up -d
```

---

## 📁 Project Structure

```
homomorphic-logistic-regression-agent/
├── agents/                  # Core agent modules (models, workers, supervisor, API)
│   ├── api.py              # FastAPI REST endpoints
│   ├── base.py             # Security, PHI guard, HMAC audit
│   ├── learning.py         # Active learning calibration engine
│   ├── llm_factory.py      # LLM provider factory
│   ├── metrics.py          # Prometheus metrics collector
│   ├── models.py           # Pydantic data models with validation
│   ├── streamer.py         # WebSocket telemetry broadcaster
│   ├── supervisor.py       # Master supervisor orchestrator
│   └── workers.py          # Specialized evaluation workers
├── he_logistic_reg/        # HE-LogisticReg engine module
│   ├── agents.py           # Domain agent implementations
│   ├── cli.py              # HE-LogisticReg CLI
│   ├── engine.py           # Core algorithmic engine
│   ├── models.py           # Data models with validation
│   └── server.py           # FastAPI server factory
├── tests/                  # Pytest test suite
│   ├── test_enrichment.py
│   ├── test_he_logistic_reg.py
│   └── test_homomorphic_logistic_regression_agent.py
├── web/index.html          # Operations console UI
├── enrichment.py           # Feature enrichment engines
├── simulator.py            # High-throughput simulation
├── cli.py                  # Main CLI entry point
├── he_logistic_reg_app.py  # HE-LogisticReg app entry
├── sample.csv              # Sample batch input
├── sample_payload.json     # Sample API payload
├── benchmark_dataset.json  # Benchmark test cases
├── Dockerfile              # Container build config
├── docker-compose.yml      # Container orchestration
└── pyproject.toml          # Project metadata and dependencies
```

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.
