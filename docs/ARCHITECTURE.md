# Architecture

SentinelForge v0.2 uses a deliberately small pipeline so a reviewer can inspect every stage without learning a proprietary abstraction layer.

## 1. Ingestion

`backend.main` accepts `.evtx`, `.json`, `.csv`, `.txt`, and `.log` uploads. The HTTP layer enforces the supported extension set and a 15 MB demo limit.

## 2. Parsing

- `backend/parsers/evtx_parser.py` converts EVTX records to XML and maps Windows event fields.
- `backend/parsers/text_parser.py` handles JSON arrays/containers, CSV, and line-oriented text.
- `backend/parsers/common.py` maps source-specific shapes into the normalized event model.

The normalizer includes aliases for common Sysmon/Wazuh fields such as `win.system.eventID`, `win.eventdata.image`, `processId`, `parentProcessId`, and network destination fields.

## 3. Detection engine

`backend/services/rule_engine.py` loads `rules/*.yml` using `yaml.safe_load`, validates a constrained schema, then evaluates clauses against normalized fields.

Supported conditions: `all`, `any`.

Supported operators: `equals`, `contains`, `startswith`, `endswith`, `regex`, `exists`.

The schema is Sigma-inspired but intentionally smaller. Full Sigma compatibility would require its complete condition grammar, modifiers, log-source taxonomy, pipelines, correlations, and backend behavior.

## 4. Correlation and enrichment

- `correlation.py` reconstructs simple PID/PPID trees per host.
- `ioc.py` extracts common indicators from the source payload.
- `scoring.py` combines detection severity and confidence into a bounded triage score.
- ATT&CK coverage is derived from detection mappings, not inferred from untrusted source text.

## 5. Presentation

One analysis result is a JSON contract consumed by both the API and browser UI. The CLI uses the same analyzer, keeping behavior consistent across interfaces.

## Non-goals in v0.2

- High-volume streaming ingestion
- Multi-tenant authentication
- Durable case storage
- SIEM query compilation
- Full Sigma compatibility
- Threat-intelligence lookups requiring external network calls

These omissions keep the portfolio release understandable and reproducible.
