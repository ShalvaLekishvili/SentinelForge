# SentinelForge architecture

```text
Browser
  │
  ├── static dashboard (HTML/CSS/JS)
  │
  └── POST /api/analyze
          │
          ▼
      FastAPI
          │
          ├── parser / normalizer
          ├── detection engine
          ├── IOC extractor
          └── risk scoring
                  │
                  ▼
             JSON result
```

## v0.1 boundaries

The MVP deliberately processes files in memory, has a 5 MB upload limit, and supports JSON/CSV/TXT/LOG. EVTX, persistent cases, authenticated users, Sigma rules, Wazuh API integration, and PDF reporting are planned for later releases.
