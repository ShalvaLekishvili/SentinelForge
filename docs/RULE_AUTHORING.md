# Rule authoring

SentinelForge rules are compact YAML documents intended to demonstrate detection-as-code engineering.

## Minimal rule

```yaml
id: SF-EXAMPLE-001
title: Example suspicious process
severity: medium
confidence: medium
description: Explain what behavior is being detected.
mitre: [T1059.001]
logsource: windows_process_creation
detection:
  condition: all
  clauses:
    - field: process
      operator: contains
      value: powershell
    - field: command_line
      operator: regex
      value: 'suspicious-pattern'
```

## Required fields

- `id` — stable project-specific identifier
- `title` — concise analyst-facing name
- `severity` — `low`, `medium`, `high`, or `critical`
- `detection.clauses` — a list of field checks

## Optional metadata

- `description`
- `confidence` — `low`, `medium`, or `high`
- `mitre` — current ATT&CK technique/sub-technique IDs
- `logsource` — human-readable source expectation

## Operators

- `equals`
- `contains`
- `startswith`
- `endswith`
- `regex`
- `exists`

A clause `value` may also be a list; a match against any value satisfies that clause.

## Review checklist

1. Use a current ATT&CK identifier and verify the behavior genuinely maps to it.
2. Prefer behavior over a single filename/hash when possible.
3. Document likely false positives in the pull request.
4. Add or update a synthetic sample/test that proves the rule fires.
5. Avoid unsafe content or real malicious payloads in repository test data.
6. Avoid pretending a broad heuristic is a high-confidence malicious verdict.

## Sigma relationship

Sigma is a substantially richer open detection format. SentinelForge deliberately borrows the idea of YAML detection-as-code and metadata separation while keeping its own small evaluator. A future release may add optional Sigma validation/import rather than silently claiming compatibility.
