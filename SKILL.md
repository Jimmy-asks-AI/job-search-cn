---
name: job-search-cn
description: "面向中国求职者的求职工作流 skill：中文/英文简历编写与美化、岗位搜索规划、JD 分析、岗位真实性判断、按岗位定制简历、投递包生成、岗位收件箱、投递日志、跟进复盘，以及带明确确认门槛的半自动/受控自动投递辅助。用于用户请求中国求职、简历优化、岗位筛选、投递准备、申请跟踪、面试准备或平台投递辅助时。"
---

# 中国求职 Skill

## 范围

用于中国求职场景，包括：

- 编写或优化面向中国雇主的中文/英文简历。
- 生成 ATS 友好的简历，必要时生成视觉版简历。
- 按岗位、城市、薪资、行业、公司黑名单、职级、远程/现场、平台等条件规划搜索。
- 分析 JD，并为单个公司-岗位定制简历。
- 判断岗位真实性：当前有效、谨慎推进、疑似虚假或未验证。
- 维护轻量岗位收件箱、投递日志、跟进节奏和面试准备笔记。
- 准备求职信、BOSS/智联/猎聘沟通话术、表单开放题拟答和确认清单。
- 执行半自动或受控自动投递辅助，但真实动作必须逐项确认。

本 skill 参考 `career-ops`、`Resume-Matcher`、`reactive-resume`、`boss-agent-cli`、`AIHawk`、`findajob`、`AutoApply` 和 `job-crawler` 的已测试模式。

## 安全边界

默认使用 **assistive 模式**。除非用户明确要求并确认最终目标清单，否则不要提交申请、发送沟通、上传简历、绕过验证码、规避反爬/风控，或操作已登录账号。

隐式触发也只能停留在 assistive 模式。请求看起来像求职任务，不等于允许使用登录页面、浏览器会话、平台账号或真实投递表单。

任何真实提交、发送或上传前，必须让用户确认：

- 平台、公司、岗位、城市、岗位 URL。
- 简历版本和将要提交的求职信/沟通文本。
- 动作序列：发送沟通、上传文件、填写表单、点击投递。
- 影响岗位数量。批量数量必须写明。

没有确认时，只能生成投递包或给出人工交接步骤。

涉及平台交互、登录态、浏览器自动化、批量动作或自动投递时，先读 [compliance_policy.md](references/compliance_policy.md)。

## 工作流

1. **需求收集**
   - 收集目标岗位、城市、行业、薪资、职级、工作模式、平台偏好、约束条件、公司/岗位黑名单。
   - 简历或 JD 缺失时，要求用户提供，或使用 `templates/` 中的模板创建。
   - 对中国候选人，只在相关时收集期望城市、薪资、到岗时间、户口/工作许可和隐私敏感联系方式。

2. **主简历整理**
   - 用 `templates/resume_master.md` 维护事实源。
   - 按 [resume_schema.md](references/resume_schema.md) 组织简历。
   - 将 Markdown 简历转成 JSON 结构时，使用 `scripts/parse_resume.py`。

3. **岗位发现**
   - 平台覆盖和能力等级见 [platform_registry.yml](references/platform_registry.yml)。
   - 优先使用用户提供的 JD 或公开只读搜索。
   - 输出搜索计划：平台、关键词、城市、筛选条件、风险等级、预期结果。
   - 多岗位任务使用 `templates/job_pipeline.md`：原始 URL/JD 放入 `Pending`，评估后移入 `Processed`，无法访问的标记为 `[!]`。
   - 区分确认有效岗位、过期岗位、未验证片段和被反爬阻断页面。除非列出来源和去重规则，不要声称“全网完整”。
   - 对 CSV/JSON/JSONL 岗位列表先用 `scripts/dedupe_jobs.py` 去重。

4. **JD 分析与匹配**
   - 按 [jd_analysis_rubric.md](references/jd_analysis_rubric.md) 分析 JD。
   - 用 `scripts/analyze_jd.py` 做本地关键词/要求初筛。
   - 用 `scripts/score_match.py` 比较简历和 JD，列出缺失关键词。
   - 分开写硬性要求、加分项、平台术语、不可验证缺口、岗位真实性信号和面试准备主题。

5. **定制简历**
   - 每个公司-岗位生成一份 `templates/resume_targeted.md` 风格的定制简历。
   - 不编造经历。只能基于用户提供的事实重排、强调、量化和改写。
   - 保留改写审计：改了什么、来源事实、对应 JD 要求、原因、风险。

6. **简历美化与导出**
   - 上传平台默认使用 ATS 友好版本：单栏、清晰标题、可选择文本、常用字体。
   - 只有雇主期待作品集/视觉呈现时才使用视觉版，并同时保留 ATS 安全版本。
   - 没有完整渲染器时，用 `scripts/render_resume.py` 从 Markdown 生成 HTML。

7. **投递包**
   - 用 `scripts/export_application_packet.py` 生成岗位投递包：简历、求职信/沟通文本、JD 分析、确认清单、日志片段。
   - 求职信和平台沟通话术使用 `templates/cover_letter_cn.md`。
   - 记录到 `templates/application_log.md` 或等价表格/数据库。
   - 批量跟进或状态分析前，用 `scripts/validate_application_log.py` 校验日志。

8. **投递或交接**
   - 普通请求：交付投递包和人工步骤。
   - 半自动请求：用户批准后只打开岗位页，最终提交由用户点击。
   - 受控自动投递：按 [application_workflow.md](references/application_workflow.md) 执行，每个真实发送/上传/提交动作都要最终确认。
   - 登录失效、验证码/风控提示、平台阻断或提交状态不明时，停止自动化，记录原因，转人工交接。

9. **复盘与迭代**
   - 投递、回复、拒绝或面试反馈后，更新投递日志。
   - 根据结果优化搜索过滤、简历 bullet、关键词、沟通话术、跟进时间和面试故事缺口。

## 输出约定

完整岗位申请任务应输出：

- `job_analysis.md` 或 JSON 等价结果。
- `match_score.json` 或清晰评分表。
- `resume_targeted_<company>_<role>.md`。
- 可选 `resume_targeted_<company>_<role>.html`、PDF 或 DOCX。
- `cover_letter_<company>_<role>.md` 或平台沟通话术。
- `application_packet/` 和最终确认清单。
- 更新后的投递日志行。
- 用户请求管线/跟进/面试时，可输出 `job_pipeline.md`、跟进草稿或面试准备笔记。

## 参考文件

- [platform_registry.yml](references/platform_registry.yml)：中国招聘平台覆盖和能力等级。
- [compliance_policy.md](references/compliance_policy.md)：安全门槛和真实动作确认。
- [resume_schema.md](references/resume_schema.md)：简历结构、版本和隐私字段。
- [jd_analysis_rubric.md](references/jd_analysis_rubric.md)：JD 解析、评分、真实性和面试准备。
- [application_workflow.md](references/application_workflow.md)：投递状态、岗位收件箱和交接规则。
- [test_matrix.md](references/test_matrix.md)：验证 skill 行为。
