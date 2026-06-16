# Compliance Policy

Use this file whenever a request touches live platforms, account login, browser automation, messages, uploads, or application submission.

## Risk Modes

| Mode | Allowed | Requires Confirmation | Forbidden |
|---|---|---|---|
| assistive | Resume/JD analysis, search plan, templates, packet generation, logs | None | Any live submit/send/upload |
| read_only | Open public or user-authorized pages, collect visible job info | Before using logged-in pages | Form submission, greeting messages |
| semi_auto | Open target pages and prefill text for user review | Before opening logged-in/apply pages | Agent clicking submit |
| controlled_auto | Submit/send/upload one confirmed item at a time | Final confirmation per item | Batch default, captcha bypass |

Default mode is `assistive`.

Implicit invocation must remain in `assistive` mode until the user explicitly chooses a higher-risk mode. Inferring that the user wants job-search help is not permission to use accounts, logged-in pages, browser sessions, or live platform forms.

## Hard Rules

- Never fabricate resume facts, credentials, employers, dates, degrees, salary, awards, or certifications.
- Never bypass captcha, rate limits, anti-bot controls, platform risk prompts, or account security checks.
- Never send messages or applications in batch unless the user supplies an explicit target list and confirms the count.
- Never reuse a resume tailored for one company on another company without re-checking JD fit.
- Never store or expose secrets, cookies, tokens, government ID numbers, or private contact data in skill files.
- When a platform's terms or UI block automation, provide manual handoff steps.

## Live Action Controls

- Treat each submit, send, upload, form fill, or click-to-apply as a separate live action unless the user confirms an explicit action sequence.
- `controlled_auto` defaults to one confirmed item at a time. Batch actions require a visible target list, visible count, and confirmation of the exact sequence.
- Stop immediately on captcha, login refresh, account-risk prompt, rate-limit warning, abnormal redirect, or ambiguous submission result.
- Do not retry a failed live action blindly. Log `blocked_by_platform`, `submit_unknown`, or `user_takeover_required`, then hand off manual steps.
- Resume version/hash should be recorded as a timestamped filename or content hash prefix, for example `resume_targeted_acme_pm_20260616_sha1abcd1234.md`.

## Confirmation Template

Before a live action, show this concise confirmation:

```text
将要执行的真实动作：
- 平台：
- 公司/岗位/城市：
- URL：
- 动作序列：发送沟通 / 上传简历 / 填写表单 / 点击投递
- 简历版本：
- 附加文本：
- 影响岗位数量：

请确认是否执行。未确认前我只生成投递包，不提交。
```

## Audit Trail

Every application-related action must write or propose a log row with:

- Timestamp.
- Platform.
- Company.
- Role.
- City.
- URL.
- Resume version/hash.
- Action mode.
- Status.
- Notes and next follow-up date.

Recommended status values:

- `packet_ready`
- `manual_handoff`
- `user_confirmed`
- `submitted`
- `blocked_by_platform`
- `submit_unknown`
- `user_takeover_required`
- `rejected`
- `no_response`
