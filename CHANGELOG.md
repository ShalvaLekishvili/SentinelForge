# Changelog

## 0.2.0 — Telemetry Engine

### Added
- EVTX parsing via python-evtx
- Wazuh/Sysmon-friendly event normalization
- external YAML rule engine with 12 defensive rules
- process tree correlation
- MITRE ATT&CK coverage summary
- domain/email IOC extraction
- CLI analysis and JSON export
- `/api/rules` endpoint
- redesigned analyst dashboard
- multi-version CI, Ruff configuration and Dependabot
- architecture, rule-authoring, demo and roadmap documentation

### Changed
- Risk scoring now combines severity with confidence.
- MITRE mappings were refreshed to current sub-technique IDs (for example, Run Keys → T1547.001).
- CORS is restricted to local development origins instead of wildcard access.

### Removed
- Python-hardcoded detection matchers from v0.1.
