"""Parse a Markdown resume into a simple JSON section map."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def parse_markdown(text: str) -> dict[str, object]:
    title = ""
    sections: dict[str, list[str]] = {}
    current = "preamble"
    sections[current] = []

    for line in text.splitlines():
        heading = re.match(r"^(#{1,3})\s+(.+?)\s*$", line)
        if heading:
            level = len(heading.group(1))
            name = heading.group(2).strip()
            if level == 1 and not title:
                title = name
            current = name
            sections.setdefault(current, [])
            continue
        sections.setdefault(current, []).append(line)

    clean_sections = {
        key: "\n".join(value).strip()
        for key, value in sections.items()
        if "\n".join(value).strip()
    }
    return {"title": title, "sections": clean_sections}


def main() -> int:
    parser = argparse.ArgumentParser(description="Parse Markdown resume sections.")
    parser.add_argument("resume", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    result = parse_markdown(args.resume.read_text(encoding="utf-8-sig"))
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        args.out.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
