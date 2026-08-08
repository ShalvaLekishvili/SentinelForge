# Research notes for v0.2

SentinelForge v0.2 was redesigned against current primary documentation rather than only extending the v0.1 code shape.

## Sigma

Sigma documents detection rules as YAML with rule metadata, log source context, and detection logic. SentinelForge adopts the **detection-as-code and YAML separation** idea but deliberately keeps a smaller local grammar and does not claim full Sigma compatibility.

- https://sigmahq.io/docs/guide/getting-started.html
- https://sigmahq.io/docs/basics/rules.html

## MITRE ATT&CK

Technique IDs in the bundled rules were checked against current ATT&CK pages. Examples:

- T1547.001 — Registry Run Keys / Startup Folder
- T1053.005 — Scheduled Task
- T1003.001 — LSASS Memory
- T1218.005 — Mshta
- T1218.010 — Regsvr32
- T1218.011 — Rundll32
- T1543.003 — Windows Service
- T1105 — Ingress Tool Transfer

Reference: https://attack.mitre.org/

## EVTX

The project uses `python-evtx`, a cross-platform pure-Python parser for Windows Event Log files. The library exposes event records as XML, which SentinelForge then maps into its normalized event schema.

- https://github.com/williballenthin/python-evtx

## FastAPI

FastAPI's `UploadFile`/multipart path is used for bounded file upload ingestion. `python-multipart` is included as a dependency as required by FastAPI's file-upload documentation.

- https://fastapi.tiangolo.com/tutorial/request-files/

## GitHub Actions

The CI workflow follows GitHub's documented Python approach: `setup-python` is used explicitly and tests are executed across a Python version matrix.

- https://docs.github.com/actions/tutorials/build-and-test-code/python
