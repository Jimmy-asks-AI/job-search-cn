"""Validate the Markdown application log without external dependencies."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


STATUSES = {
    "collected",
    "screened",
    "evaluated",
    "tailored",
    "packet_ready",
    "manual_handoff",
    "user_confirmed",
    "submitted",
    "in_conversation",
    "responded",
    "interview",
    "offer",
    "accepted",
    "rejected",
    "no_response",
    "follow_up_7d",
    "follow_up_14d",
    "follow_up_30d",
    "blocked_by_platform",
    "submit_unknown",
    "user_takeover_required",
    "skipped",
    "discarded",
}

LEGITIMACY = {"high_confidence", "caution", "suspicious", "unverified"}
REQUIRED = {"日期", "平台", "公司", "岗位", "城市", "链接", "匹配分", "状态"}


def cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_placeholder(value: str) -> bool:
    return not value or value.startswith("{{") or value.endswith("}}")


def parse_table(text: str) -> tuple[list[str], list[list[str]]]:
    lines = [line for line in text.splitlines() if line.strip().startswith("|")]
    if len(lines) < 2:
        return [], []
    header = cells(lines[0])
    rows = []
    for line in lines[2:]:
        row = cells(line)
        if len(row) == len(header):
            rows.append(row)
    return header, rows


def validate(text: str) -> list[str]:
    header, rows = parse_table(text)
    if not header:
        return ["No Markdown table found."]
    missing = REQUIRED - set(header)
    errors = [f"Missing columns: {', '.join(sorted(missing))}"] if missing else []
    index = {name: header.index(name) for name in header}
    seen = set()

    for line_no, row in enumerate(rows, start=3):
        data = {name: row[pos] for name, pos in index.items()}
        if any(is_placeholder(value) for value in data.values()):
            continue

        status = data.get("状态", "")
        if status not in STATUSES:
            errors.append(f"line {line_no}: invalid status '{status}'")

        legitimacy = data.get("真实性", "")
        if legitimacy and legitimacy not in LEGITIMACY:
            errors.append(f"line {line_no}: invalid legitimacy '{legitimacy}'")

        score = data.get("匹配分", "")
        if score and not re.fullmatch(r"\d{1,3}(/100)?", score):
            errors.append(f"line {line_no}: invalid score '{score}'")
        if score:
            value = int(score.split("/")[0])
            if value > 100:
                errors.append(f"line {line_no}: score over 100")

        key = (data.get("链接") or "", data.get("公司") or "", data.get("岗位") or "", data.get("城市") or "")
        if key in seen:
            errors.append(f"line {line_no}: duplicate application key")
        seen.add(key)
    return errors


def self_test() -> None:
    sample = """| 日期 | 平台 | 公司 | 岗位 | 城市 | 链接 | 匹配分 | 真实性 | 状态 |
|---|---|---|---|---|---|---:|---|---|
| 2026-07-02 | boss | A | PM | 深圳 | https://x | 80/100 | caution | evaluated |
"""
    assert validate(sample) == []
    assert validate(sample.replace("evaluated", "done"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate application log markdown.")
    parser.add_argument("log", nargs="?", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        print("self-test OK")
        return 0
    if not args.log:
        parser.error("log path required unless --self-test is used")
    errors = validate(args.log.read_text(encoding="utf-8-sig"))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("application log OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
