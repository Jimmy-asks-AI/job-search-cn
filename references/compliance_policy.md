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

## Hard Rules

- Never fabricate resume facts, credentials, employers, dates, degrees, salary, awards, or certifications.
- Never bypass captcha, rate limits, anti-bot controls, platform risk prompts, or account security checks.
- Never send messages or applications in batch unless the user supplies an explicit target list and confirms the count.
- Never reuse a resume tailored for one company on another company without re-checking JD fit.
- Never store or expose secrets, cookies, tokens, government ID numbers, or private contact data in skill files.
- When a platform's terms or UI block automation, provide manual handoff steps.

## Confirmation Template

Before a live action, show this concise confirmation:

```text
将要执行的真实动作：
- 平台：
- 公司/岗位/城市：
- URL：
- 动作类型：发送沟通 / 上传简历 / 填写表单 / 点击投递
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
