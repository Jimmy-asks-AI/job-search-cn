"""Compare a resume against a JD and output a transparent keyword score."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


STOPWORDS = {
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
    "简历",
    "项目",
    "公司",
}

KNOWN_TERMS = [
    "产品经理",
    "用户增长",
    "数据分析",
    "数据看板",
    "用户分层",
    "增长策略",
    "跨团队协作",
    "互联网产品",
    "b端",
    "saas",
    "sql",
    "a/b",
    "ab实验",
    "a/b实验",
    "python",
    "java",
    "go",
    "javascript",
    "typescript",
    "react",
    "vue",
    "fastapi",
    "django",
    "spring",
    "机器学习",
    "深度学习",
    "大模型",
    "nlp",
    "推荐系统",
    "风控",
    "量化",
    "本科",
    "硕士",
    "博士",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def tokens(text: str) -> set[str]:
    found = set()
    lowered = text.lower()
    for term in KNOWN_TERMS:
        if term.lower() in lowered:
            found.add(term.lower())
    for item in re.findall(r"[A-Za-z][A-Za-z0-9+#.\-]{1,}", text):
        token = item.lower().strip()
        if token and token not in STOPWORDS:
            found.add(token)
    if found:
        return found
    for item in re.findall(r"[\u4e00-\u9fff]{2,8}", text):
        token = item.lower().strip()
        if token and token not in STOPWORDS:
            found.add(token)
    return found


def score(resume_text: str, jd_text: str) -> dict[str, object]:
    resume_tokens = tokens(resume_text)
    jd_tokens = tokens(jd_text)
    if not jd_tokens:
        ratio = 0.0
        matched = set()
    else:
        matched = resume_tokens & jd_tokens
        ratio = len(matched) / len(jd_tokens)

    missing = sorted(jd_tokens - resume_tokens)
    present = sorted(matched)
    score_value = round(ratio * 100)
    if score_value >= 85:
        label = "strong_fit"
    elif score_value >= 70:
        label = "good_fit"
    elif score_value >= 55:
        label = "weak_fit"
    else:
        label = "low_fit"

    return {
        "score": score_value,
        "label": label,
        "matched_keywords": present[:100],
        "missing_keywords": missing[:100],
        "resume_keyword_count": len(resume_tokens),
        "jd_keyword_count": len(jd_tokens),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Score resume/JD keyword overlap.")
    parser.add_argument("--resume", required=True, type=Path)
    parser.add_argument("--jd", required=True, type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    result = score(read(args.resume), read(args.jd))
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        args.out.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
