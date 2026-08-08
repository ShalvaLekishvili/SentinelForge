# SentinelForge Detection Rules

Rules are YAML documents loaded from this directory at startup. The schema is intentionally small and **Sigma-inspired**, not a claim of full Sigma compatibility.

Each rule contains metadata (`id`, `title`, `severity`, `confidence`, optional MITRE ATT&CK technique IDs) and a `detection` section with `all` or `any` clause logic. Supported clause operators are `equals`, `contains`, `startswith`, `endswith`, `regex`, and `exists`.

See [`docs/RULE_AUTHORING.md`](../docs/RULE_AUTHORING.md) before contributing a rule.
