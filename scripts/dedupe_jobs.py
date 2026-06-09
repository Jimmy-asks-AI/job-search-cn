"""Deduplicate job lists from CSV, JSON array, or JSONL files."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any


def load_rows(path: Path) -> list[dict[str, Any]]:
    suffix = path.suffix.lower()
    text = path.read_text(encoding="utf-8-sig")
    if suffix == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle))
    if suffix == ".jsonl":
        return [json.loads(line) for line in text.splitlines() if line.strip()]
    if suffix == ".json":
        data = json.loads(text)
        if isinstance(data, list):
            return data
        if isinstance(data, dict) and isinstance(data.get("jobs"), list):
            return data["jobs"]
    raise ValueError(f"Unsupported input format: {path}")


def norm(value: Any) -> str:
    text = str(value or "").lower()
    text = re.sub(r"https?://", "", text)
    text = re.sub(r"[\s\-_/#?&=]+", "", text)
    return text


def pick(row: dict[str, Any], *names: str) -> str:
    lowered = {str(key).lower(): value for key, value in row.items()}
    for name in names:
        if name in row and row[name]:
            return str(row[name])
        if name.lower() in lowered and lowered[name.lower()]:
            return str(lowered[name.lower()])
    return ""


def key_for(row: dict[str, Any]) -> tuple[str, str, str, str]:
    company = pick(row, "company", "公司", "company_name")
    title = pick(row, "title", "岗位", "职位", "job_title", "position")
    city = pick(row, "city", "城市", "location")
    url = pick(row, "url", "链接", "job_url", "link")
    if url:
        return ("url", norm(url), "", "")
    return ("fields", norm(company), norm(title), norm(city))


def dedupe(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen = set()
    output = []
    for row in rows:
        key = key_for(row)
        if key in seen:
            continue
        seen.add(key)
        output.append(row)
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="Deduplicate job list.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    rows = dedupe(load_rows(args.input))
    with args.out.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(json.dumps({"input": str(args.input), "output": str(args.out), "rows": len(rows)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
