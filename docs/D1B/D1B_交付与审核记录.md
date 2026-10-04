# D1B v0.3 交付与审核记录

设计日期2026-10-01；工具链最后修订2026-10-04。ContractVersion 4 Draft；DatabaseSchemaVersion 独立且尚未分配；Gate 0 未通过，待非作者 R 复核。

## 2026-10-04 Review 闭环范围

本轮只加固生成器、自动回归与证据。14 条 finding 的逐项实现和复核入口见 [评审修改报告](D1B_评审修改报告.md)；原 CV4 业务设计、字段能力、Profile 规则、模板值和控件数不变。SVG 使用原 Mermaid 的完整节点与业务边，保留既有图表色彩与 CSS；语义 placeholder 渲染后正文业务文字不变。

机器摘要在默认中文 Windows / cp936 环境下统一 UTF-8；六份 tracked 产物继续只包含固定输入与声明规范。实际 Python/平台/stdout/UTF-8 mode 记录在仓库外本轮验证材料中；它们不进入生成物，避免跨机 drift。

验证矩阵覆盖正常 build、只读 check、原有输入反例与新反例、cp936 的 clean/drift/缺文件报告、危险链接无外部 exists 探测、简单成员 parser、initial_focus、SVG/Mermaid、Windows autocrlf 检出与 Diff 格式。所有数量从实际 JSON 读取；旧“两项回归”是历史记录，本轮套件以实际输出为准。

本轮保留未暂存 Diff 供人工审核，建议一次提交 `fix: 加固D1B生成器跨编码与验证边界`，获授权后一次 push 至现有 #3。发布后的远端 head、PR body、闭环评论及 R Review 按相应授权处理；本文不虚构 clean commit、push 或 Approval。

## 固定内容身份与动态发布身份

SP1_BASELINE_ANCHOR `a0dfdd8e373ae90f765c20cf8c075a8754f674bd`；PR #8 已 APPROVED 并合并，OD-0002 Accepted。目标 Windows 7 SP1 / 6.1.7601 x86/x64；需求/规划 v2.1、SP1 任务台账与其三份新指纹由生成器核验。业务工作簿指纹不变；schema_types.hpp 与原 CV4 完全相同，HEADER_SHA 保留。

contract candidate `e8ad944e7c9c8df77c7c5fd883c4459a75270e92`、PR2 final review head `f47fa3e251d5fa02f077a6cf9f39feeebf15d3f4` 分别保留。固定内容锚点不表示 current main、阶段 head 或 merge-base；动态 Git 身份、Draft/Ready、推送和 Review 以 PR #3 正文、发布快照和 Formal Review 为准。

## 2026-10-03 清单处理

| 项目 | 单一源变更与证据 | 验收边界 |
| --- | --- | --- |
| 平台与整合 | #3 的平台状态已按本轮请求恢复 Draft；main→阶段基线 integration 材料另存本轮交付快照 | 实际状态以 GitHub 为准；整合/发布/Review 按对应授权与平台结果，不在此固化动态状态 |
| SP1目标 | 正文、DPI、RV09、Q10 使用 Windows 7 SP1 / 6.1.7601 x86/x64 | C 的 Guest、字体/DPI/打印机证据仍独立验收 |
| v2.1来源 | 需求/规划、SP1台账、OD-0002与handoff链接固定到内容锚点 | OD仅覆盖OS，不改DTO/API/CV/主发行架构 |
| 受控指纹 | 三份 v2.1 新SHA、业务工作簿原SHA与schemaSHA实际核验 | 不修改当前分支或目录外的 Word/Excel 原件 |
| Q1/Q2决定 | 单业务工作簿；P1行1/52标题与P2行3/23标题均首期Source Profile | 不代表ImportProfile冻结、详细映射/值域批准或已完成D3 |
| Q01/Q02/Q05 | 删除业务范围未决；保留日期/枚举/状态、数据级脱敏测试样本、5 Unsupported与8语义项 | HEADER-ONLY、0数据行；不复制未合并#6详细草案 |
| P11/P12只读提示 | 使用既有P11-03/P12-09显示首期范围与未冻结状态 | 不增加可写frozen标志，不改变预检信任边界或操作控件 |
| 防回退 | SP1/7601/v2.1/OD/handoff/Q项/SourceProfile冻结区分新增静态检查 | 当前数量以证据JSON实际重算，旧统计仅历史 |
| 反例 | SP1→RTM、7601→7600、v2.1SHA→旧SHA、旧Q项重插、范围冒充冻结 | 故意损坏输入必须失败；旧CV4反例保留 |
| HTML | 源重建，CSS/结构不重构，增量目视记录随本轮交付快照 | 只验设计文档，不冒充Win7程序UI实测 |

## 逐文件原因

| 文件 | 原因 |
| --- | --- |
| 生成/设计正文.md | SP1/v2.1/OD/handoff来源、Q01/Q02/Q05/Q10/RV09、固定内容与动态身份分开 |
| 生成/设计数据.json | 两Source Profile范围、HEADER-ONLY与未冻结元数据；既有控件只读提示 |
| 生成/build_design.py | SP1内容锚点、三新SHA、防回退检查、交付身份移除动态Git值 |
| 生成/test_build_design.py | 新环境/指纹/Owner决定/冻结区分反例，保留原CV4与漂移零写入回归 |
| README/本记录/评审修改报告 | 长期来源与职责说明、SP1同步章节，删除容易过时的动态Git快照 |
| 设计MD/HTML及四JSON证据 | 六份产物由源重建，按实际输入重算 |

`.gitattributes`、CSS、34字段、Tag、27/28显式映射、FieldChange、可信预检、派生人数、筛选/日期/状态/报告等 CV4 主体不改。业务样表、公共契约、Gate及A/C文件未修改。

## 验证身份与范围

生成器核验四份受控/样表指纹及契约指纹；静态/交付/输入核查数量与结果见当前 JSON，不继承上一轮数量。`--check`逐字节比较六份产物且零写入；两项回归验证故意回退拒绝、临时副本漂移非零退出且不写入。

阶段分支纳入SP1前，可在独立非Git验证副本中，以固定锚点的受控资料验证候选源及产物；这种候选检查不表示阶段Git整合完成，也不代替纳入/发布后的实际head复验。本轮外部快照明确记载验证目录、输入指纹、命令/退出码、实际Git状态和增量目视范围。

2026-10-02 的1024/800目录/SVG/长表/键盘/链接与print CSS完整检查保留为历史；2026-10-03本轮仅增量核验SP1/7601、Q01/Q02/Q05/Q10、OD/handoff链接与长表溢出。未做实际打印预览分页/实物打印、缺字体环境、Win32、导入事务或Windows 7 SP1 VM验收。

## 协作与交还

A/D3/R：Profile冻结和唯一匹配、详细逐列处置、5 Unsupported、8语义项、枚举/状态/重复候选及批准证据；A/R：候选筛选、搜索、状态更正、报告接口；甲方：数据级脱敏测试样本与模板意向。C：VS2017/v141_xp、Windows 7 SP1 / 6.1.7601 x86/x64、字体/DPI/设备/GDI/xlsx证据。R：在最终push后对实际head走RV01–RV09并提交Formal Review。

建议提交：`docs: 同步D1B的SP1基线与首期Source Profile决定`。阶段成果仅#3；整合经GitHub PR，不本地merge/rebase、不强推。提交、发布、integration创建及其合并各依明确授权；成果切Ready并请求R须在最后push与behind=0核验后。任何Approval不等于Gate 0 PASS。
