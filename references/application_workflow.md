# Application Workflow

Use this file for packet creation, status tracking, and apply/handoff decisions.

## States

```text
collected -> screened -> tailored -> packet_ready -> user_confirmed -> submitted
                                     -> manual_handoff
                                     -> skipped
user_confirmed -> in_conversation -> submitted
submitted -> interview -> offer -> accepted
submitted -> rejected -> re_tailor -> screened
submitted -> no_response -> follow_up_7d -> follow_up_14d -> follow_up_30d
any_live_action -> blocked_by_platform -> manual_handoff
any_live_action -> submit_unknown -> verify_status -> manual_handoff
```

## Packet Contents

Each company-role packet should contain:

- JD snapshot and source URL.
- Match score and gap notes.
- Tailored resume.
- Cover letter or platform greeting.
- Upload filename recommendation.
- Manual application steps.
- Final confirmation checklist.
- Log row.

## Auto-Apply Gates

Gate 1: target list is deduped and visible to the user.  
Gate 2: each job has a tailored resume and message.  
Gate 3: user sees final content and confirms.  
Gate 4: agent submits only the confirmed action or confirmed action sequence.
Gate 5: result is logged immediately.

If any gate fails, stop at `packet_ready` or `manual_handoff`.

## Failure Handling

- If captcha, risk prompt, login refresh, account challenge, rate-limit warning, or UI block appears, stop at `blocked_by_platform` and give manual steps.
- If the page changes but success is not visible, log `submit_unknown` and ask the user to verify the platform status.
- If the user wants to continue in the browser after a block, switch to `user_takeover_required`; do not keep clicking.
- For rejection or poor response feedback, move to `re_tailor`, update the JD gap notes, and only then reuse the company-role packet.

## Action Sequence

For each confirmed live action, record:

- `action_sequence`: ordered list such as `open_page -> fill_form -> upload_resume -> user_review -> submit`.
- `confirmed_count`: number of affected jobs.
- `resume_version_hash`: filename or short content hash of the submitted resume.
- `fallback_mode`: `manual_handoff` when the platform blocks automation.

## Platform Message Style

For BOSS/智联/猎聘-style greetings:

- 80-160 Chinese characters.
- Mention role fit in one sentence.
- Mention one concrete project/skill match.
- Ask for further communication politely.
- Avoid exaggerated claims and mass-message tone.

Example:

```text
您好，我关注到贵司的{{岗位}}岗位。我有{{年限/领域}}经验，做过{{项目/成果}}，与JD中的{{关键词}}比较匹配。已准备好针对该岗位的简历，方便的话希望进一步沟通。
```
