# Security policy

SentinelForge is a defensive analysis project.

## Supported release

Security fixes target the latest release on `main`.

## Reporting a vulnerability

Please report security issues privately to the repository owner rather than opening a public issue containing exploit details or sensitive data.

## Data handling

- Do not commit real incident logs, credentials, tokens, customer identifiers, or malware samples.
- Use synthetic or sanitized telemetry for issues and pull requests.
- Core analysis does not require outbound internet access.
- Uploaded files are analyzed in memory or temporary local files; v0.2 does not implement persistent case storage.

## Scope

The project detects and explains suspicious behaviors. Contributions that turn SentinelForge into offensive automation are outside project scope.
