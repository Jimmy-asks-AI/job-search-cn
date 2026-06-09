"""Render a Markdown resume to a styled HTML file without external deps."""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path


ATS_CSS = """
body { font-family: Arial, "Microsoft YaHei", sans-serif; color: #111; margin: 36px auto; max-width: 820px; line-height: 1.48; }
h1 { font-size: 26px; margin: 0 0 14px; border-bottom: 2px solid #111; padding-bottom: 8px; }
h2 { font-size: 18px; margin: 22px 0 8px; border-bottom: 1px solid #ccc; padding-bottom: 4px; }
h3 { font-size: 15px; margin: 14px 0 6px; }
p, li { font-size: 13px; }
ul { margin: 6px 0 12px 20px; padding: 0; }
table { border-collapse: collapse; width: 100%; font-size: 12px; }
th, td { border: 1px solid #ddd; padding: 6px; vertical-align: top; }
"""

VISUAL_CSS = """
body { font-family: "Microsoft YaHei", Arial, sans-serif; color: #172033; margin: 0; background: #f5f7f8; }
main { max-width: 900px; margin: 28px auto; background: #fff; padding: 42px 52px; box-shadow: 0 10px 28px rgba(20,30,45,.10); }
h1 { font-size: 30px; margin: 0 0 16px; color: #0f3d5e; }
h2 { font-size: 18px; margin: 24px 0 10px; color: #0f3d5e; border-left: 4px solid #1f7a8c; padding-left: 10px; }
h3 { font-size: 15px; margin: 16px 0 6px; color: #172033; }
p, li { font-size: 13px; line-height: 1.55; }
ul { margin: 6px 0 12px 20px; padding: 0; }
table { border-collapse: collapse; width: 100%; font-size: 12px; }
th, td { border: 1px solid #d9e2e7; padding: 6px; vertical-align: top; }
"""


def inline_markdown(text: str) -> str:
    value = html.escape(text)
    value = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", value)
    value = re.sub(r"`(.+?)`", r"<code>\1</code>", value)
    return value


def markdown_to_html(text: str) -> str:
    lines = text.splitlines()
    output: list[str] = []
    in_ul = False

    def close_ul() -> None:
        nonlocal in_ul
        if in_ul:
            output.append("</ul>")
            in_ul = False

    for line in lines:
        stripped = line.strip()
        if not stripped:
            close_ul()
            continue
        heading = re.match(r"^(#{1,3})\s+(.+)$", stripped)
        if heading:
            close_ul()
            level = len(heading.group(1))
            output.append(f"<h{level}>{inline_markdown(heading.group(2))}</h{level}>")
            continue
        if stripped.startswith(("- ", "* ")):
            if not in_ul:
                output.append("<ul>")
                in_ul = True
            output.append(f"<li>{inline_markdown(stripped[2:])}</li>")
            continue
        close_ul()
        output.append(f"<p>{inline_markdown(stripped)}</p>")

    close_ul()
    return "\n".join(output)


def render(markdown: str, style: str) -> str:
    css = VISUAL_CSS if style == "visual" else ATS_CSS
    body = markdown_to_html(markdown)
    wrapper_start = "<main>" if style == "visual" else ""
    wrapper_end = "</main>" if style == "visual" else ""
    return f"<!doctype html>\n<html lang=\"zh-CN\">\n<head>\n<meta charset=\"utf-8\">\n<style>{css}</style>\n</head>\n<body>\n{wrapper_start}\n{body}\n{wrapper_end}\n</body>\n</html>\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Render Markdown resume to HTML.")
    parser.add_argument("resume", type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--style", choices=["ats", "visual"], default="ats")
    args = parser.parse_args()

    html_text = render(args.resume.read_text(encoding="utf-8-sig"), args.style)
    args.out.write_text(html_text, encoding="utf-8")
    print(str(args.out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
