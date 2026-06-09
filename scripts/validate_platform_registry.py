"""Dependency-free structural validation for platform_registry.yml."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


REQUIRED_KEYS = {
    "id",
    "name",
    "domains",
    "priority",
    "category",
    "capability_level",
    "supports",
    "requires_login_for",
    "default_mode",
    "risk",
}


def parse_blocks(text: str) -> list[tuple[int, str]]:
    matches = list(re.finditer(r"(?m)^  - id:\s*([^\n#]+)", text))
    blocks: list[tuple[int, str]] = []
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        line_no = text[:start].count("\n") + 1
        blocks.append((line_no, text[start:end]))
    return blocks


def validate(text: str) -> list[str]:
    errors: list[str] = []
    if "platforms:" not in text:
        errors.append("Missing top-level 'platforms:' key.")
        return errors
    blocks = parse_blocks(text)
    if not blocks:
        errors.append("No platform entries found.")
        return errors
    ids = set()
    for line_no, block in blocks:
        keys = set(re.findall(r"(?m)^    ([a-zA-Z_]+):", block))
        entry_id_match = re.search(r"^  - id:\s*([^\n#]+)", block, re.MULTILINE)
        entry_id = entry_id_match.group(1).strip().strip('"') if entry_id_match else f"line-{line_no}"
        if entry_id in ids:
            errors.append(f"Duplicate id '{entry_id}' at line {line_no}.")
        ids.add(entry_id)
        missing = sorted(REQUIRED_KEYS - keys - {"id"})
        if missing:
            errors.append(f"Platform '{entry_id}' line {line_no} missing keys: {', '.join(missing)}")
        level = re.search(r"capability_level:\s*(\d+)", block)
        if level and not 0 <= int(level.group(1)) <= 4:
            errors.append(f"Platform '{entry_id}' has invalid capability_level.")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate platform registry.")
    parser.add_argument("registry", type=Path)
    args = parser.parse_args()

    errors = validate(args.registry.read_text(encoding="utf-8-sig"))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("platform_registry.yml OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
