"""Lightweight JD analyzer for job-search-cn.

This script is intentionally dependency-free. It does not replace LLM analysis;
it provides a local first pass for keywords, requirements, risks, and metadata.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


HARD_PATTERNS = [
    "本科",
    "硕士",
    "博士",
    "学历",
    "必须",
    "必备",
    "至少",
    "年以上",
    "经验",
    "熟练",
    "精通",
    "掌握",
    "证书",
    "英语",
]

PREFERRED_PATTERNS = ["优先", "加分", "最好", "熟悉", "了解", "有.*经验者"]
RESP_PATTERNS = ["负责", "参与", "推动", "建设", "设计", "优化", "维护", "协同"]
RISK_PATTERNS = ["培训费", "押金", "无责底薪", "大小周", "996", "狼性", "抗压", "外包", "驻场", "薪资面议"]

KNOWN_TERMS = [
    "产品经理",
    "用户增长",
    "数据分析",
    "数据看板",
    "用户分层",
    "增长策略",
    "跨团队协作",
    "互联网产品",
    "B端",
    "SaaS",
    "SQL",
    "A/B",
    "Python",
    "Java",
    "Go",
    "JavaScript",
    "TypeScript",
    "React",
    "Vue",
    "FastAPI",
    "Django",
    "Spring",
    "机器学习",
    "深度学习",
    "大模型",
    "NLP",
    "推荐系统",
    "风控",
    "量化",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def split_lines(text: str) -> list[str]:
    lines: list[str] = []
    for raw in re.split(r"[\n\r]+|(?<=[。；;])", text):
        line = re.sub(r"\s+", " ", raw).strip(" -*\t")
        if line:
            lines.append(line)
    return lines


def contains_any(line: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, line, re.IGNORECASE) for pattern in patterns)


def extract_keywords(text: str, limit: int = 80) -> list[str]:
    tokens: dict[str, int] = {}
    lowered = text.lower()
    for term in KNOWN_TERMS:
        if term.lower() in lowered:
            tokens[term] = tokens.get(term, 0) + 3
    for item in re.findall(r"[A-Za-z][A-Za-z0-9+#.\-]{1,}|[\u4e00-\u9fff]{2,8}", text):
        token = item.strip().lower()
        if len(token) < 2:
            continue
        tokens[token] = tokens.get(token, 0) + 1
    stop = {
        "岗位",
        "职责",
        "要求",
        "工作",
        "能力",
        "相关",
        "以及",
        "进行",
        "负责",
        "优先",
        "经验",
    }
    ranked = sorted(
        ((token, count) for token, count in tokens.items() if token not in stop),
        key=lambda pair: (-pair[1], pair[0]),
    )
    return [token for token, _ in ranked[:limit]]


def guess_metadata(text: str) -> dict[str, str]:
    metadata = {}
    salary = re.search(r"(\d+[kK千万wW][-~至]\d+[kK千万wW]|\d+[-~至]\d+[kK千万wW])", text)
    if salary:
        metadata["salary"] = salary.group(1)
    years = re.search(r"(\d+\s*[-~至]?\s*\d*)\s*年(?:以上)?", text)
    if years:
        metadata["experience_years"] = years.group(0)
    degree = re.search(r"(大专|本科|硕士|博士|研究生)", text)
    if degree:
        metadata["degree"] = degree.group(1)
    return metadata


def analyze(text: str) -> dict[str, object]:
    lines = split_lines(text)
    hard = [line for line in lines if contains_any(line, HARD_PATTERNS)]
    preferred = [line for line in lines if contains_any(line, PREFERRED_PATTERNS)]
    responsibilities = [line for line in lines if contains_any(line, RESP_PATTERNS)]
    risks = [line for line in lines if contains_any(line, RISK_PATTERNS)]
    keywords = extract_keywords(text)
    return {
        "metadata": guess_metadata(text),
        "hard_requirements": hard[:30],
        "preferred_requirements": preferred[:30],
        "responsibilities": responsibilities[:40],
        "risk_items": risks[:20],
        "keywords": keywords,
        "line_count": len(lines),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze a Chinese job description.")
    parser.add_argument("jd", type=Path, help="Path to a JD text/markdown file.")
    parser.add_argument("--out", type=Path, help="Optional JSON output path.")
    args = parser.parse_args()

    result = analyze(read_text(args.jd))
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        args.out.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
