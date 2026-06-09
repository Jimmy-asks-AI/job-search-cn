---
name: job-search-cn
description: "Use this skill for China-focused job search workflows: Chinese resume writing and beautification, JD analysis, domestic job-platform search planning, resume tailoring per role, application packet creation, application tracking, and controlled auto-apply assistance with explicit user confirmation."
---

# Job Search CN

## Scope

Use this skill when the user wants help with a China-focused job search, including:

- Writing or improving a Chinese/English resume for Chinese employers.
- Rendering a polished ATS-friendly resume or a visual resume.
- Finding jobs by role, city, salary, industry, company blacklist, seniority, remote/on-site, or platform.
- Analyzing a JD and tailoring a resume for that specific role.
- Preparing cover letters, BOSS/智联/猎聘 greeting messages, application notes, and tracking logs.
- Performing semi-automatic or controlled automatic application steps.

This skill is based on tested patterns from `career-ops`, `Resume-Matcher`, `reactive-resume`, `boss-agent-cli`, `AIHawk`, `findajob`, `AutoApply`, and `job-crawler`.

## Safety Boundary

Default to **assistive mode**. Do not submit applications, send greetings, upload resumes, bypass captchas, evade anti-bot systems, or operate a logged-in account unless the user explicitly asks for that exact action and confirms the final target list.

Before any real submit/send/upload action, require a final confirmation containing:

- Platform, company, role, city, and job URL.
- Resume version and cover/greeting text to be submitted.
- Whether the action sends a message, uploads a file, fills a form, or clicks submit.
- Count of applications affected. Batch count must be explicit.

If confirmation is missing, stop at application-packet generation or browser-assisted handoff.

Read [compliance_policy.md](references/compliance_policy.md) before any platform interaction, login-state use, browser automation, batch operation, or auto-apply request.

## Workflow

1. **Intake**
   - Gather target role, city, industry, salary, seniority, work mode, preferred platforms, constraints, and company/title blacklists.
   - If the resume or JD is missing, ask for it or create a template from `templates/`.
   - For Chinese candidates, capture expected city, salary, availability, hukou/work authorization only when relevant, and privacy-sensitive contact fields.

2. **Resume Base**
   - Use `templates/resume_master.md` for the master resume.
   - Structure the resume with [resume_schema.md](references/resume_schema.md).
   - Use `scripts/parse_resume.py` when converting a Markdown resume into a JSON section map.

3. **Job Discovery**
   - For platform coverage and capability levels, read [platform_registry.yml](references/platform_registry.yml).
   - Prefer manual JD input or public read-only search first.
   - Build a search plan with platform, query, city, filters, risk level, and expected output.
   - Use `scripts/dedupe_jobs.py` for CSV/JSON/JSONL job lists before scoring or application.

4. **JD Analysis And Matching**
   - Analyze JD using [jd_analysis_rubric.md](references/jd_analysis_rubric.md).
   - Use `scripts/analyze_jd.py` for a lightweight local keyword/requirement pass.
   - Use `scripts/score_match.py` to compare a resume with a JD and surface missing keywords.
   - Separate hard requirements, preferred requirements, platform-specific terms, and unverifiable gaps.

5. **Targeted Resume**
   - Create one tailored resume per company-role pair from `templates/resume_targeted.md`.
   - Do not invent experience. Reorder, emphasize, quantify, and rephrase only from supplied facts.
   - Include a change log: changed sentence, source resume fact, JD requirement, reason, and risk.

6. **Beautification And Export**
   - Use ATS-friendly layout for upload: single column, clear headings, selectable text, common fonts.
   - Use visual layout only when the employer expects portfolio-style presentation.
   - Use `scripts/render_resume.py` to create a styled HTML resume from Markdown when no full resume renderer is available.

7. **Application Packet**
   - Use `scripts/export_application_packet.py` to create a per-job packet with resume, cover letter, greeting, JD analysis, and confirmation checklist.
   - Use `templates/cover_letter_cn.md` for cover letters and platform messages.
   - Track every action in `templates/application_log.md` format or an equivalent table/database.

8. **Apply Or Handoff**
   - For normal requests, deliver the packet and exact manual steps.
   - For semi-automatic requests, open the job page only after user approval and let the user click submit.
   - For controlled auto-apply, follow [application_workflow.md](references/application_workflow.md) and require final confirmation for every submit/send/upload action.

9. **Review And Iterate**
   - After application or rejection feedback, update the application log and extract lessons.
   - Refine search filters, resume bullets, keywords, and greeting text.

## Output Contract

For a complete job application task, produce:

- `job_analysis.md` or JSON equivalent.
- `match_score.json` or a clear score table.
- `resume_targeted_<company>_<role>.md`.
- Optional `resume_targeted_<company>_<role>.html` or PDF/DOCX if renderer is available.
- `cover_letter_<company>_<role>.md` or platform greeting.
- `application_packet/` with final checklist.
- Updated application log entry.

## References

- Use [platform_registry.yml](references/platform_registry.yml) for China platform coverage and capability levels.
- Use [compliance_policy.md](references/compliance_policy.md) for safety gates.
- Use [resume_schema.md](references/resume_schema.md) for resume structure and privacy fields.
- Use [jd_analysis_rubric.md](references/jd_analysis_rubric.md) for JD parsing and scoring.
- Use [application_workflow.md](references/application_workflow.md) for apply-state transitions.
- Use [test_matrix.md](references/test_matrix.md) when validating skill behavior.
