from __future__ import annotations

import argparse
import json
from pathlib import Path

from backend.services.analyzer import analyze_bytes


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze telemetry with SentinelForge")
    parser.add_argument("file", type=Path)
    parser.add_argument("--output", type=Path, help="Write JSON result to a file")
    args = parser.parse_args()

    data = args.file.read_bytes()
    result = analyze_bytes(data, args.file.suffix.lower(), args.file.name)
    rendered = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
