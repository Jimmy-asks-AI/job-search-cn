# JD Analysis Rubric

Use this file for job-description parsing, matching, and resume tailoring.

## Extract

Produce:

- Company, role, city, platform, URL, publish date when available.
- Work mode: remote, hybrid, onsite.
- Seniority and years of experience.
- Hard requirements: degree, years, required skills, industry background, certificates, language.
- Preferred requirements: tools, domain, extra skills, leadership, cross-functional work.
- Responsibilities.
- Keywords: Chinese terms, English terms, tools, methods, business domains.
- Risk items: unclear salary, outsourcing, 996 hints, training fees, suspicious contact, unrealistic requirements.
- Posting legitimacy signals: publish/update date, recruiter activity, JD specificity, salary range spread, repeated reposts, and company risk news when available.

## Score

Use a transparent 100-point score:

- Hard requirements: 40.
- Core skills and tools: 25.
- Domain/industry fit: 15.
- Impact evidence and metrics: 10.
- Location/salary/availability fit: 10.

Classify:

- `85-100`: Strong fit; tailor and apply.
- `70-84`: Good fit; tailor with gap notes.
- `55-69`: Weak fit; apply only if strategic.
- `<55`: Skip unless user requests.

## Posting Legitimacy

Classify each posting:

- `high_confidence`: current posting, concrete JD, credible salary range, no obvious risk signal.
- `caution`: mixed signals, stale date, broad salary range, vague team/product detail, or company risk needs user review.
- `suspicious`: expired/inaccessible page, unrealistic requirements, training fee, suspicious contact, or repeated repost pattern.

Do not overclaim. If sources are weak, write `unverified` and keep the job out of auto-apply.

## Interview Prep Extract

For roles scored `70+`, also extract:

- Top 5 likely interview topics from the JD.
- 3-6 STAR+R story prompts grounded in the resume facts.
- Application-form questions likely to appear, such as motivation, salary, availability, relocation, work authorization, and open-ended fit questions.

## Tailoring Rules

Allowed:

- Reorder relevant experience.
- Rephrase existing facts using JD language.
- Add metrics already present in source material.
- Split dense bullets into JD-aligned bullets.
- Move less relevant details to lower priority.

Not allowed:

- Invent employers, dates, titles, degrees, projects, metrics, tools, certificates, or publications.
- Claim hands-on experience when the source only shows exposure.
- Hide hard requirement gaps.

## Change Log Format

| Section | Before | After | JD Basis | Source Fact | Risk |
|---|---|---|---|---|---|

If source facts are missing, write `needs_user_input` instead of inventing.
