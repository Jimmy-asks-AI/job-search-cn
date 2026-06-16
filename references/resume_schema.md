# Resume Schema

Use this schema for Chinese candidate resumes. Keep master facts separate from tailored wording.

## Master Profile Fields

Required:

- `name`
- `phone`
- `email`
- `city`
- `target_roles`
- `target_cities`
- `availability`
- `work_authorization`
- `education`
- `experience`
- `projects`
- `skills`

Optional:

- `wechat`
- `portfolio`
- `github`
- `linkedin`
- `expected_salary`
- `current_status`
- `certifications`
- `languages`
- `publications`
- `awards`
- `campus_experience`

Sensitive fields:

- Government ID, exact home address, family details, current salary proof, references, private photos, certificates with ID numbers, account tokens, and private contact channels not intended for employers.
- Store only when the user explicitly asks; never send by default.

## Resume Versioning

Every tailored resume should have a traceable version:

- Filename pattern: `resume_targeted_<company>_<role>_<yyyymmdd>_<hash>.md`.
- Hash can be the first 8-12 characters of a local content hash.
- Record the source master resume version, JD URL/snapshot date, and change log.
- Do not include secrets, government ID numbers, or raw private notes in filenames or hashes.

## Experience Item

```yaml
company:
title:
location:
start:
end:
industry:
team:
scope:
bullets:
  - action:
    context:
    metric:
    tools:
    evidence:
```

## Bullet Quality

Prefer bullets that include:

- Action verb.
- Business or technical context.
- Scope: users, revenue, volume, team size, data size, frequency.
- Measurable result.
- Tools, methods, or domain keywords.

Avoid:

- Empty adjectives such as “负责相关工作”.
- Claims not supported by source facts.
- Stacking unrelated keywords in one sentence.

## China-Specific Resume Notes

- One-page is preferred for junior candidates; two pages are acceptable for experienced candidates.
- ATS upload version should be simple, selectable text, single column, and common fonts.
- Visual version can be used for design, product, marketing, or portfolio-led roles, but keep an ATS upload version when the platform parses resumes.
- Expected salary, availability, and target city are often useful but should be omitted when they weaken negotiation.
