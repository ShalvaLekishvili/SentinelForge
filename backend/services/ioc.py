from __future__ import annotations

import re

PATTERNS = {
    "ipv4": re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b"),
    "url": re.compile(r"https?://[^\s\"'<>]+", re.I),
    "sha256": re.compile(r"\b[a-fA-F0-9]{64}\b"),
    "sha1": re.compile(r"\b[a-fA-F0-9]{40}\b"),
    "md5": re.compile(r"\b[a-fA-F0-9]{32}\b"),
}


def extract_iocs(text: str) -> dict[str, list[str]]:
    result = {}
    for name, pattern in PATTERNS.items():
        result[name] = sorted(set(pattern.findall(text)))[:100]
    return result
