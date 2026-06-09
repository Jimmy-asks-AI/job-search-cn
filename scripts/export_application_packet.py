"""Create a per-job application packet folder."""

from __future__ import annotations

import argparse
import shutil
from datetime import date
from pathlib import Path


def safe_part(value: str) -> str:
    keep = []
    for char in value.strip():
        if char.isalnum() or char in ("-", "_"):
            keep.append(char)
        elif char.isspace():
            keep.append("-")
    return "".join(keep).strip("-_") or "unknown"


def copy_if_present(source: Path | None, target: Path) -> None:
    if source and source.exists():
        shutil.copyfile(source, target)


def main() -> int:
    parser = argparse.ArgumentParser(description="Export application packet.")
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--company", required=True)
    parser.add_argument("--role", required=True)
    parser.add_argument("--platform", default="")
    parser.add_argument("--city", default="")
    parser.add_argument("--url", default="")
    parser.add_argument("--resume", type=Path)
    parser.add_argument("--jd-analysis", type=Path)
    parser.add_argument("--cover-letter", type=Path)
    args = parser.parse_args()

    folder_name = f"{date.today().isoformat()}_{safe_part(args.company)}_{safe_part(args.role)}"
    packet = args.out_dir / folder_name
    packet.mkdir(parents=True, exist_ok=True)

    copy_if_present(args.resume, packet / "resume_targeted.md")
    copy_if_present(args.jd_analysis, packet / "job_analysis.json")
    copy_if_present(args.cover_letter, packet / "cover_letter.md")

    checklist = f"""# Application Packet Checklist

- Company: {args.company}
- Role: {args.role}
- Platform: {args.platform}
- City: {args.city}
- URL: {args.url}
- Date: {date.today().isoformat()}

## Before Submission

- [ ] JD snapshot reviewed.
- [ ] Resume version reviewed.
- [ ] Cover letter or greeting reviewed.
- [ ] No invented facts.
- [ ] User confirmed live action.

## Live Action Confirmation

Do not submit/send/upload until the user confirms this exact packet.
"""
    (packet / "confirmation_checklist.md").write_text(checklist, encoding="utf-8")

    log_row = (
        f"| {date.today().isoformat()} | {args.platform} | {args.company} | {args.role} | "
        f"{args.city} | {args.url} |  | {packet.name} | assistive | packet_ready |  |  |\n"
    )
    (packet / "application_log_row.md").write_text(log_row, encoding="utf-8")
    print(str(packet))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
