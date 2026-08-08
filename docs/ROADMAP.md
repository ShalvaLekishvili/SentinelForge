# SentinelForge roadmap

## v0.2 — Telemetry Engine ✅

- EVTX ingestion
- Wazuh/Sysmon normalization aliases
- YAML detection rules
- process correlation
- ATT&CK coverage
- CLI + API + redesigned analyst UI
- CI/lint/testing baseline

## v0.3 — Detection Quality

- event-type aware rule pre-filtering
- field alias catalog
- rule unit-test fixtures
- investigation text search
- severity/confidence tuning documentation
- more Sysmon event semantics

## v0.5 — Investigation Workspace

- persisted local cases (SQLite)
- analyst notes and status
- detection acknowledgement
- evidence tags
- timeline filters
- case summary export

## v0.7 — Interoperability

- Wazuh alert adapter
- optional Sigma validation/import experiment
- HTML incident report
- STIX-friendly IOC export experiment

## v1.0 — Stable Portfolio Release

- stable normalized schema
- migration/versioning policy
- expanded synthetic incident pack
- accessibility and UI polish pass
- release artifacts and demo recording
- contribution governance

## Explicitly out of scope

SentinelForge is not intended to automate intrusion, persistence, credential theft, exploitation, or evasion. Detection examples may recognize those behaviors in telemetry, but the project should remain defensive and analysis-focused.
