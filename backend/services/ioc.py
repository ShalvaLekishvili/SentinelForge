from __future__ import annotations

import ipaddress
import re

PATTERNS = {
    "url": re.compile(r"https?://[^\s\"'<>]+", re.I),
    "domain": re.compile(r"\b(?=.{4,253}\b)(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[A-Za-z]{2,63}\b"),
    "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,63}\b"),
    "sha256": re.compile(r"\b[a-fA-F0-9]{64}\b"),
    "sha1": re.compile(r"\b[a-fA-F0-9]{40}\b"),
    "md5": re.compile(r"\b[a-fA-F0-9]{32}\b"),
}
IPV4 = re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b")


def _valid_ipv4(text: str) -> list[str]:
    values: set[str] = set()
    for match in IPV4.findall(text):
        try:
            ipaddress.ip_address(match)
            values.add(match)
        except ValueError:
            continue
    return sorted(values)[:100]


def extract_iocs(text: str) -> dict[str, list[str]]:
    result = {name: sorted(set(pattern.findall(text)))[:100] for name, pattern in PATTERNS.items()}
    result["ipv4"] = _valid_ipv4(text)
    return result
