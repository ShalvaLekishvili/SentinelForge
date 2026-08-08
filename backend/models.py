from __future__ import annotations

from typing import Any
from pydantic import BaseModel, Field


class NormalizedEvent(BaseModel):
    id: int
    timestamp: str = ""
    host: str = ""
    user: str = ""
    event_id: str = ""
    channel: str = ""
    process: str = ""
    process_id: str = ""
    parent_process: str = ""
    parent_process_id: str = ""
    command_line: str = ""
    destination_ip: str = ""
    destination_port: str = ""
    raw: dict[str, Any] = Field(default_factory=dict)


class Detection(BaseModel):
    rule_id: str
    title: str
    description: str = ""
    severity: str
    confidence: str = "medium"
    mitre: list[str] = Field(default_factory=list)
    event_id: int
    timestamp: str = ""
    host: str = ""
    user: str = ""
    process: str = ""
    command_line: str = ""
    evidence: list[str] = Field(default_factory=list)


class AnalysisResult(BaseModel):
    analysis_id: str
    source: str
    parser: str
    event_count: int
    detection_count: int
    risk: dict[str, Any]
    detections: list[Detection]
    iocs: dict[str, list[str]]
    timeline: list[NormalizedEvent]
    process_tree: list[dict[str, Any]]
    mitre_coverage: list[dict[str, Any]]
    metadata: dict[str, Any] = Field(default_factory=dict)
