# Contributing

Contributions are welcome when they improve defensive investigation, detection quality, parsers, tests, documentation, or accessibility.

## Local checks

```bash
python -m pip install -r requirements-dev.txt
ruff check backend tests
pytest
```

## Detection rule pull requests

Include:

- rationale and expected telemetry source
- verified MITRE ATT&CK mapping
- severity and confidence reasoning
- expected false positives
- a synthetic positive fixture/test

Do not include live credentials, private incident data, weaponized payloads, or malware samples.
