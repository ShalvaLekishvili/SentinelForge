from __future__ import annotations

import csv
import io
import json
from typing import Any


def parse_json(text: str) -> list[dict[str, Any]]:
    payload = json.loads(text)
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict):
        for key in ("events", "data", "alerts", "hits"):
            value = payload.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
        return [payload]
    return []


def parse_csv(text: str) -> list[dict[str, Any]]:
    return list(csv.DictReader(io.StringIO(text)))


def parse_lines(text: str) -> list[dict[str, Any]]:
    return [{"message": line.strip()} for line in text.splitlines() if line.strip()]
