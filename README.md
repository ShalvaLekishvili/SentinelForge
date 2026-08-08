# SentinelForge

**Forge raw security telemetry into actionable intelligence.**

SentinelForge is an open-source SOC investigation and detection engineering workbench for analyzing structured security telemetry, surfacing suspicious behavior, extracting indicators of compromise, and presenting an analyst-friendly investigation timeline.

> **Status:** `v0.1.0 MVP` — portfolio-grade foundation under active development.

## What exists today

- FastAPI backend and health endpoint
- JSON / CSV / TXT / LOG ingestion
- Normalized investigation timeline
- Eight behavior-based detection rules
- IOC extraction for IPv4, URLs, MD5, SHA-1 and SHA-256
- Risk scoring and severity summary
- Responsive enterprise-style SOC dashboard
- Built-in synthetic incident demo
- Pytest test suite
- Docker and GitHub Actions CI
- GitHub Projects bootstrap script and development backlog

## Detection coverage

| Rule | Behavior | Severity | MITRE ATT&CK |
|---|---|---:|---|
| SF-EXEC-001 | Encoded PowerShell | High | T1059.001 |
| SF-EXEC-002 | Office → PowerShell | High | T1204.002 / T1059.001 |
| SF-PERS-001 | Registry Run Key | Medium | T1060 / T1547.001 |
| SF-PERS-002 | Scheduled Task creation | Medium | T1053.005 |
| SF-CRED-001 | Potential LSASS dump | Critical | T1003.001 |
| SF-DEF-001 | Defender tampering | High | T1562.001 |
| SF-EXEC-003 | Executable from AppData/Temp | Medium | T1204.002 |
| SF-LOLBIN-001 | Suspicious LOLBin usage | Medium | T1218 |

## Quick start

### Python

```bash
git clone https://github.com/ShalvaLekishvili/SentinelForge.git
cd SentinelForge
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

Open `http://127.0.0.1:8000`, click **Load demo**, then **Analyze**.

### Docker

```bash
docker compose up --build
```

## Repository map

```text
backend/                 FastAPI + parsing + detections + IOC + scoring
frontend/                SOC dashboard
rules/                   future external rule schema
sample-data/             sanitized / synthetic telemetry
tests/                   unit tests
scripts/bootstrap_github.sh
                         creates the GitHub Project scaffolding
docs/                    architecture + project backlog
.github/                 CI + issue templates
```

## Roadmap

**v0.2 — Telemetry Engine**  
EVTX ingestion, Sysmon normalization, external YAML detection rules.

**v0.5 — Investigation Workspace**  
Process trees, case persistence, filtering, analyst notes, MITRE views.

**v0.8 — Reporting & Integrations**  
HTML/PDF reports, Wazuh alert adapter, export pipelines.

**v1.0 — Stable Release**  
Hardened deployment, expanded tests, polished documentation and reproducible demo investigations.

## GitHub Project setup

A ready-made script is included:

```bash
chmod +x scripts/bootstrap_github.sh
./scripts/bootstrap_github.sh
```

It uses the official GitHub CLI to create/link **SentinelForge — Development Roadmap**, add custom fields, and seed initial draft work items. Review the script before running it because it writes to your GitHub account.

## Safety and scope

SentinelForge is built for defensive security analysis, training, detection engineering, and incident investigation. Demo data in this repository is synthetic. Never commit production secrets or sensitive incident artifacts.

## License

MIT © 2026 Shalva Lekishvili
