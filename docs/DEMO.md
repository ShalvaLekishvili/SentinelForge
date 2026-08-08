# Demo investigation

The bundled `sample-data/demo-incident.json` is synthetic. It represents a common investigation narrative without shipping executable payloads or real malicious infrastructure.

## Narrative

1. A user opens a macro-enabled document.
2. Word spawns PowerShell with an encoded-command argument.
3. PowerShell retrieves a synthetic file from a `.invalid` domain.
4. A synthetic child executable starts.
5. `schtasks.exe` creates a logon task.
6. PowerShell attempts to disable real-time monitoring.

## Analyst questions

- Which parent process created the suspicious PowerShell process?
- Which ATT&CK techniques were mapped by detections?
- Which external indicators were extracted?
- Which process is the common ancestor of persistence and defense-tampering activity?

This dataset is suitable for screenshots, UI demos, tests, and portfolio walkthroughs.
