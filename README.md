# job-search-cn

面向中国求职者的 Codex skill，用于把求职流程拆成可追踪、可审计、可确认的工作流：简历辅助编写、简历美化、岗位搜索规划、JD 分析、按岗位定制简历、生成投递包，以及带强确认门槛的半自动/受控自动投递辅助。

## 能做什么

- **简历辅助编写**：从主简历整理结构化信息，改写经历 bullet，补齐求职信息缺口。
- **简历美化**：把 Markdown 简历渲染为 ATS 友好的 HTML，也提供视觉版样式入口。
- **按需求寻找岗位**：根据目标岗位、城市、薪资、行业、平台、黑名单生成搜索计划，并支持岗位列表去重。
- **JD 分析与匹配**：抽取硬性要求、加分项、职责、关键词、风险项，并输出简历/JD 匹配分。
- **岗位管线**：维护轻量岗位收件箱，区分待评估、已处理、已阻断岗位。
- **定制简历**：针对每个公司和岗位生成定制简历，并要求保留改写审计，避免虚构经历。
- **投递包生成**：生成每个岗位的简历、JD 分析、求职信/沟通话术、确认清单和投递日志行。
- **投递后复盘**：支持状态、真实性、跟进日期和面试准备信息的日志化。
- **投递辅助**：支持手动投递、半自动打开页面、受控自动投递的流程设计；真实发送、上传、提交前必须逐项确认。

## 最近优化内容

参考 `career-ops` 后，本 skill 增加了更完整但仍保持轻量的求职管线：

- `templates/job_pipeline.md`：岗位收件箱，用于区分待评估、已处理和已阻断岗位。
- `references/jd_analysis_rubric.md`：新增岗位真实性判断，输出 `high_confidence`、`caution`、`suspicious` 或 `unverified`。
- `templates/application_log.md`：新增“真实性”列，并扩展投递状态。
- `scripts/validate_application_log.py`：本地校验投递日志状态、评分和重复岗位。
- `scripts/export_application_packet.py`：导出的投递包清单和日志片段已包含真实性与表单拟答检查项。

没有引入 `career-ops` 的 Node/Playwright/Go dashboard/插件系统；当前仓库仍保持 Python 标准库脚本和确认式投递边界。

## 安全边界

默认模式是 `assistive`：只分析、生成、整理，不执行真实投递。

不会默认执行以下动作：

- 登录招聘平台。
- 发送 BOSS/智联/猎聘沟通消息。
- 上传简历。
- 填写并提交真实表单。
- 批量投递。
- 绕过验证码、反爬、风控或平台限制。

真实提交前必须展示平台、公司、岗位、URL、简历版本、附加文本、影响数量，并获得用户最终确认。

## 支持的平台和渠道

当前 skill 内置的是**平台能力注册表和工作流规则**，不是对所有平台都已经实现真实爬虫。

`references/platform_registry.yml` 中包含：

- BOSS 直聘
- 智联招聘
- 前程无忧 / 51job
- 猎聘
- 拉勾
- 脉脉
- 牛客
- 实习僧
- 应届生求职网
- 国聘
- Moka 企业招聘
- 北森招聘
- 大易招聘

每个平台记录能力等级、默认模式、支持动作、登录要求和风险等级。平台动作默认停在搜索规划、详情解析、投递包生成或手动交接；真实投递必须确认。

## 目录结构

```text
job-search-cn/
  SKILL.md
  agents/
    openai.yaml
  references/
    application_workflow.md
    compliance_policy.md
    jd_analysis_rubric.md
    platform_registry.yml
    resume_schema.md
    test_matrix.md
  scripts/
    analyze_jd.py
    dedupe_jobs.py
    export_application_packet.py
    parse_resume.py
    render_resume.py
    score_match.py
    validate_application_log.py
    validate_platform_registry.py
  templates/
    application_log.md
    application_packet_checklist.md
    candidate_profile.yml
    cover_letter_cn.md
    job_pipeline.md
    job_search_brief.md
    platform_adapter.md
    resume_master.md
    resume_targeted.md
```

## 脚本

所有脚本均为本地运行，只使用 Python 标准库，不会访问招聘平台。

```powershell
python scripts/analyze_jd.py jd.md --out job_analysis.json
python scripts/score_match.py --resume resume.md --jd jd.md --out match_score.json
python scripts/parse_resume.py resume.md --out resume_sections.json
python scripts/render_resume.py resume.md --out resume.html --style ats
python scripts/dedupe_jobs.py jobs.csv --out jobs_dedup.jsonl
python scripts/export_application_packet.py --out-dir packets --company 示例科技 --role 产品经理 --resume resume.md --jd-analysis job_analysis.json
python scripts/validate_application_log.py templates/application_log.md
python scripts/validate_platform_registry.py references/platform_registry.yml
```

## 安装到 Codex

把整个目录复制到本机 Codex skills 目录：

Windows PowerShell:

```powershell
Copy-Item -Recurse . "$env:USERPROFILE\.codex\skills\job-search-cn"
```

macOS / Linux:

```bash
mkdir -p "$HOME/.codex/skills"
cp -R . "$HOME/.codex/skills/job-search-cn"
```

然后在 Codex 里用：

```text
用 $job-search-cn 帮我分析这个岗位 JD，并按它改一版简历。
```

## 参考项目

本 skill 的设计参考了以下开源项目。参考方式是功能理解和架构借鉴；本仓库没有直接复制这些项目的代码。

| 项目 | 仓库 | 借鉴点 |
|---|---|---|
| career-ops | https://github.com/santifer/career-ops | 本地文件驱动的求职操作系统、简历/门户/投递日志、doctor/verify/dedup/PDF 输出 |
| Resume-Matcher | https://github.com/srbhr/Resume-Matcher | JD 匹配、关键词缺口、ATS 视角、简历定制工作流 |
| reactive-resume | https://github.com/amruthpillai/reactive-resume | 结构化简历 schema、模板化渲染、PDF/DOCX/可视化简历能力 |
| boss-agent-cli | https://github.com/can4hou6joeng4/boss-agent-cli | 中国招聘平台适配、BOSS/智联/51job 思路、低风险合规边界、CLI schema |
| Jobs_Applier_AI_Agent_AIHawk | https://github.com/feder-cr/Jobs_Applier_AI_Agent_AIHawk | 自动投递代理流程、岗位 URL 到定制简历/求职信的链路、浏览器代理风险边界 |
| findajob | https://github.com/brockamer/findajob | 自托管求职管线、状态管理、申请材料生成、反馈学习和成本统计 |
| AutoApply-AI-Agentic-Browser-Automation-for-Job-Search | https://github.com/Rayyan9477/AutoApply-AI-Agentic-Browser-Automation-for-Job-Search | FastAPI + React 产品化结构、ATS 模块、投递队列、平台适配器和分析面板 |
| job-crawler | https://github.com/tengx7/job-crawler | 国内招聘网站岗位采集、平台规则、任务调度、数据中心和 Excel 导出思路 |

## 已测试情况

创建 skill 前，对上述 8 个参考项目做过本地测试，测试文件在工作区的以下文档中：

- `测试流程.md`
- `测试结果.md`
- `各部分功能理解.md`

测试结论只用于设计参考，不表示本 skill 已集成这些项目的完整代码或平台自动化能力。

## GitHub 上传前检查

建议上传前执行：

```powershell
$env:PYTHONUTF8='1'; python C:\Users\81901\.codex\skills\.system\skill-creator\scripts\quick_validate.py .
python scripts/validate_platform_registry.py references/platform_registry.yml
python scripts/validate_application_log.py --self-test
python -m compileall -q scripts
```

如果 `compileall` 生成 `scripts/__pycache__`，上传前删除它。

## 许可证

本仓库使用 MIT License，见 `LICENSE`。

参考项目仅用于功能理解和架构借鉴；本仓库没有直接复制参考项目代码。
