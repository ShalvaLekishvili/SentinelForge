# SentinelForge v0.2.0 — Telemetry Engine

This release turns the v0.1 MVP into a more credible detection-engineering portfolio project.

## Highlights

- Windows EVTX ingestion
- Wazuh/Sysmon-friendly normalization
- 12 external YAML detection rules
- current ATT&CK mappings for bundled detections
- severity + confidence risk model
- process PID/PPID correlation
- ATT&CK coverage and expanded IOC extraction
- redesigned enterprise-style analyst console
- CLI, API rule inventory and JSON export
- 15 passing tests
- multi-version GitHub Actions CI configuration
- Dependabot, PR template, research notes, architecture and roadmap docs

## Breaking changes from v0.1

- The old Python-hardcoded `detector.py` is removed.
- Detection rules now live under `rules/*.yml`.
- `mitre` is represented as a list of technique IDs.
- Analysis results now include `parser`, `process_tree`, `mitre_coverage`, and `metadata`.

## Demo

```bash
python -m pip install -r requirements-dev.txt
uvicorn backend.main:app --reload
```

Open `http://127.0.0.1:8000`, click **Load demo**, then **Run analysis**.
