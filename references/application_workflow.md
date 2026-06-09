# Application Workflow

Use this file for packet creation, status tracking, and apply/handoff decisions.

## States

```text
collected -> screened -> tailored -> packet_ready -> user_confirmed -> submitted
                                     -> manual_handoff
                                     -> skipped
submitted -> interview -> offer -> accepted
submitted -> rejected
submitted -> no_response -> follow_up
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
Gate 4: agent submits only the confirmed action.  
Gate 5: result is logged immediately.

If any gate fails, stop at `packet_ready` or `manual_handoff`.

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
