# Test Matrix

Use this file when validating changes to the skill or running a job-search workflow.

## Skill File Validation

- `SKILL.md` has YAML frontmatter with `name` and `description`.
- `agents/openai.yaml` has quoted strings and a default prompt mentioning `$job-search-cn`.
- Platform registry contains required keys for every platform.
- Python scripts compile with `python -m py_compile`.

## Workflow Validation

| Capability | Minimum Evidence |
|---|---|
| Resume writing | Master resume template filled or improvement notes produced |
| Resume beautification | HTML/PDF/DOCX output or renderer-ready Markdown with style choice |
| Job search | Search plan or collected job list with platform and filters |
| JD analysis | Hard/preferred requirements, keywords, risks, score |
| Tailored resume | Targeted resume plus change log tied to JD facts |
| Application packet | Resume, cover/greeting, checklist, log row |
| Auto-apply | Confirmation gate shown before submit/send/upload |

## Safety Validation

- No live submit/send/upload without final confirmation.
- No invented resume facts.
- No captcha bypass or anti-bot evasion.
- Every real action has an audit log row.
