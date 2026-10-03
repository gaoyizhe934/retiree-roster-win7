# D1B 使用流程与模板设计（CV4 / SP1）

阶段/轨道：D1B，v0.3；设计日期2026-10-01，最后修订2026-10-03。ContractVersion 4 Draft；DatabaseSchemaVersion 独立且尚未分配；Gate 0 未通过，待非作者 R 复核。

固定内容锚点：SP1_BASELINE_ANCHOR `a0dfdd8e373ae90f765c20cf8c075a8754f674bd`，来自已 APPROVED 并合并的 PR #8；目标 Windows 7 SP1 / 6.1.7601 x86/x64，需求说明和开发规划 v2.1、SP1 修订的任务台账。OD-0002 Accepted 只覆盖目标 OS，不改变业务 DTO/API、ContractVersion 或 Win32/x86 主发行架构。

contract candidate `e8ad944e7c9c8df77c7c5fd883c4459a75270e92`、PR2 final review head `f47fa3e251d5fa02f077a6cf9f39feeebf15d3f4` 是独立固定身份；PR2/PR8 合并均不表示 Gate 0 PASS。current main、PR #3 head、merge-base、ahead/behind 和平台 Draft/Ready 由 GitHub PR 正文、发布快照及 Formal Review 固定，长期文档不复制这些动态值。

- [离线 HTML](D1B_使用流程与模板设计.html)、[设计稿](D1B_使用流程与模板设计.md)：同源页面、字段、Tag、筛选、快照与三模板。
- [交付审核记录](D1B_交付与审核记录.md)、[评审修改报告](D1B_评审修改报告.md)：逐项变更、复核入口和边界。
- [正文源](生成/设计正文.md)、[数据源](生成/设计数据.json)、[生成器](生成/build_design.py)、[反例与回归](生成/test_build_design.py)。
- [控件数据](证据/控件与模板数据.json)、[静态检查](证据/静态核查结果.json)、[交付检查](证据/交付核查结果.json)、[输入反例](证据/生成器反例核查结果.json)。检查数量按当前输入重算。

```text
python docs/D1B/生成/build_design.py
python docs/D1B/生成/build_design.py --check
python docs/D1B/生成/test_build_design.py
```

`--check` 内存重建六份产物并逐字节比较，漂移/失败返回1且零写入；输入指纹和固定内容锚点见交付 JSON。D1B 内 `.gitattributes` 固定 HTML LF，保留 Windows autocrlf=true 的检出复现性。

Q1-B：首期只有当前业务工作簿；Q2-A：P1=Sheet1行1/52标题、P2=行3/23标题均为首期 Source Profile。范围确认不等于 ImportProfile 冻结，当前仍未冻结并进入 P12；工作簿 HEADER-ONLY、0 数据行。5个Unsupported、8个机器无法确认的映射语义及批准/值域仍待 A/D3/R，数据级脱敏测试样本仍需补充。

CV4 主体保持：27/28 显式映射、FieldChange payload/clear、可信 preview/checked copy、派生 total_count()、YearCount shape、候选白名单/类型比较、Unknown空白/disabled、既有状态日期单入口、报告默认禁用和搜索待 A/R。

D1B 成果继续使用 [PR #3](https://github.com/gaoyizhe934/retiree-roster-win7/pull/3)；远程分支 v3 是历史名称。最新 main 通过基线 integration PR 纳入阶段分支，不使用本地 merge/rebase、强推或重建成果 PR；每次合并须用户单独授权和必要评审。本轮候选及整合/发布状态以本地交付快照和 GitHub 为准。

作者静态检查及 HTML 增量目视不代表 Win32、导入事务、GDI/xlsx、实物打印或 Win7 SP1 VM 验收。权威来源见固定锚点的基线说明、OD-0002、SP1_BASELINE_HANDOFF 与 Gate Status。
