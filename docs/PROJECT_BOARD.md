# SentinelForge — GitHub Project backlog

Use this file as the seed for **SentinelForge — Development Roadmap** in GitHub Projects.

## Done · v0.2

- [x] SF-001 FastAPI service + analyst dashboard
- [x] SF-002 JSON / CSV / TXT / LOG parsers
- [x] SF-003 Windows EVTX parser integration
- [x] SF-004 Wazuh/Sysmon field normalization
- [x] SF-005 External YAML detection rule engine
- [x] SF-006 12-rule defensive detection library
- [x] SF-007 PID/PPID process graph
- [x] SF-008 IOC extraction + ATT&CK coverage
- [x] SF-009 CLI analysis + JSON export
- [x] SF-010 Multi-version CI + test suite

## Ready · v0.3 Detection Quality

- [ ] SF-101 Add logsource-aware pre-filtering to rules
- [ ] SF-102 Add field alias catalog and normalized schema version
- [ ] SF-103 Add per-rule positive/negative fixtures
- [ ] SF-104 Add investigation full-text search
- [ ] SF-105 Add timeline filters by host/user/event ID
- [ ] SF-106 Add rule false-positive metadata
- [ ] SF-107 Add Sysmon Event IDs 1/3/7/10/11/13 semantic helpers
- [ ] SF-108 Add CI rule validation command

## Backlog · v0.5 Investigation Workspace

- [ ] SF-201 Persist cases locally with SQLite
- [ ] SF-202 Add analyst notes and case status
- [ ] SF-203 Add detection acknowledgement workflow
- [ ] SF-204 Add evidence tags/bookmarks
- [ ] SF-205 Add HTML investigation report export

## Research · v0.7 Interoperability

- [ ] SF-301 Wazuh alert adapter fixtures
- [ ] SF-302 Evaluate optional Sigma validation/import
- [ ] SF-303 Evaluate STIX-compatible IOC export
- [ ] SF-304 Define normalized schema migration strategy

## Suggested project views

1. **Roadmap** — group by Release, use Start/Target Date.
2. **Engineering Board** — group by Status.
3. **Detection Lab** — filter Component = Detection.
4. **v0.3 Release** — filter Release = v0.3 and group by Priority.

## Suggested fields

- Status: Backlog / Ready / In Progress / Review / Done
- Priority: P0 / P1 / P2 / P3
- Component: API / Parser / Detection / Correlation / UI / Docs / DevOps
- Release: v0.2 / v0.3 / v0.5 / v0.7 / v1.0
- Difficulty: S / M / L / XL
- Start Date
- Target Date
