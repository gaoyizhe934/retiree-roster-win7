# Gate 0 当前复核交接

更新日期：2026-10-03。PR #2 已在 f47fa3e 获 R Formal APPROVED，并合并为 main `567d9cd32befc2b8aa7ae99487f8b6d2170f1436`。固定 contract_candidate_sha 仍为 e8ad944；下文 PR #2 的待复核步骤是当时的历史，不再作为当前执行指令。

本次新的基线修订须单独评审。当前 C-G0-03 目标是 Windows 7 SP1 / 6.1.7601，x86/x64、00_Base 与无额外运行库环境；依据 [OD-0002](../decisions/OD-0002-Windows7-SP1目标基线.md)，替代旧 RTM 条款。C-G0-01 的 VS2017/v141_xp/Win32/C++14/MT/API level 和六个消费者不变；C-G0-02 仍待 D2 工程。

Q1-B/Q2-A 已由创建者直接回答；只解决业务工作簿数量及两套 Source Profile 的首期地位。A #6 配套修改、B #3 同源重建、C #7 Guest/来源证据仍按[跨轨交接](SP1_BASELINE_HANDOFF.md)处理。当前 Gate 状态见 [GATE_STATUS](GATE_STATUS.md)。

Windows 7 SP1 基线修订由 [PR #8](https://github.com/gaoyizhe934/retiree-roster-win7/pull/8) 承载。其 review_head、base、merge-base 及作者检查身份以 GitHub PR 正文、对应 Formal Review 和实际 HEAD 生成的 evidence JSON 为准；tracked 文档不追写当前 HEAD。历史检查数字不冒充新提交结果，旧 Approval 不覆盖本次范围。Gate 0 仍未通过。

PR #8 的复核范围为 OD-0002、两份 v2.1 Word、七阶段任务台账的 OS 条款、当前入口/状态文档、基线指纹及 [SP1 二进制语义差异证据](../evidence/D1-SP1/01_受控基线OOXML语义差异.md)。该范围不适用下方 PR #2 历史中的“仅两份状态文档”限制。

---

## PR #2 证据身份修复交接原文（历史）

日期：2026-10-02。阶段 PR 仍为 #2；D1B 后续材料归入唯一有效 #3，旧 #1 已关闭。依据：[R Formal Review](https://github.com/gaoyizhe934/retiree-roster-win7/pull/2#pullrequestreview-5389158602)及创建者提供的证据身份漂移解决方案。

公共契约候选基线（contract_candidate_sha）：
`e8ad944e7c9c8df77c7c5fd883c4459a75270e92`。

该技术候选已提交并推送，包含 ContractVersion 4（Draft）以及 R01／R03／R04／R05 的契约加固；R02 保留为 D3 Application Service 的后续验收责任。作者侧在该候选上实际完成 structure 7/7、cpp14 8/8、diff 1/1、all 15/15，具体记录见[返工报告](STABILIZATION_REVIEW.md)及其发布评论。该报告保留旧审核快照，不用其中历史 SHA 或未提交表述代替此处的候选身份。

contract_candidate_sha 固定标识最后一个修改公共契约、contract tests 和 Gate0 runner 的技术候选，不能描述为本文自己的“当前 HEAD”。之后仅同步状态／证据的文档提交不会改变该候选基线。实际 review_head 由 GitHub PR 当前 HEAD、PR 正文、Formal Review 的 commit identity 和在该提交运行的 evidence JSON 共同固定；tracked 文档不追写自身提交 SHA。

### R Formal Review 状态

2026-10-02，非作者 R 已针对上述契约候选提交 [GitHub Formal Review](https://github.com/gaoyizhe934/retiree-roster-win7/pull/2#pullrequestreview-5389158602)，结论为 CHANGES_REQUESTED。

该 Review 确认 R01／R03／R04／R05 的契约级加固成立，R02 正确保留为 D3 后续验收；未发现新的契约级 P0/P1。唯一阻塞项是 Gate 状态、handoff 和 PR 正文中的证据身份仍部分指向旧提交。

本轮只同步两份状态文档与 PR 正文。同步提交发布并完成当前 HEAD 证据检查后，需要正式非作者 R 针对新的 GitHub PR HEAD 再提交 Formal Review；本文件不声明该阻塞已获 R 关闭或已 APPROVE。作者不能切换角色自签，辅助审查不能替代 Formal Review。

### C 轨正式工具链请求

本表为可领取的合作材料，尚未发送外部消息或获得 C 接收确认；状态为待 C 领取／执行，不写成已验证。

| 编号 | 工作与验收 | 状态 |
| --- | --- | --- |
| C-G0-01 | VS2017 15.9／v141_xp／Win32 x86／C++14／`/MT`／WINVER=0x0601／_WIN32_WINNT=0x0601，编译并运行下面六个消费者，保存逐项命令、退出、诊断和输入指纹 | 待正式工具链复核 |
| C-G0-02 | D2 正式工程建立后，CMake 与 XMake 使用同一头文件、宏、运行库与目标，核对编译一致性 | 待 D2 工程 |
| C-G0-03 | Win7 RTM x86 与 x64 6.1.7600、00_Base 快照，无 Office／.NET／VC++ Redistributable，保存 VS2017／v141_xp 环境记录 | 待 C 环境证据 |

消费者：

1. tests/contract/consumer_contract_test.cpp
2. tests/contract/preview_revision_test.cpp
3. tests/contract/input_authority_test.cpp
4. tests/contract/enum_field_mapping_test.cpp
5. tests/contract/field_change_test.cpp
6. tests/contract/filter_shape_test.cpp

MinGW GCC 6.3.0 的补充检查不能替代上述正式验收。原始资料 SHA-256、base／merge-base／新 HEAD、编译器完整版本与每条命令须随 C 输出保存。不要继承上一轮或 D1B 静态检查数字。

### Review Target 身份验证

发布状态／证据同步提交后，先取得真实 HEAD，再按下面的身份链固定正式复核对象：

1. 当前 GitHub PR HEAD 与本地 HEAD 一致，PR 正文的 review_head 与二者一致。
2. base／merge-base 核对为 main 基线 af0ae01981ac3d65653921ceada1cee605de5607；若基线发生变化，先重新核对，不套用旧证据。
3. `git diff --name-status e8ad944e7c9c8df77c7c5fd883c4459a75270e92..HEAD` 只能包含 docs/status/GATE0_REVIEW_HANDOFF.md 与 docs/status/GATE_STATUS.md 的状态／证据同步。
4. 公共契约、contract tests、Gate0 runner、业务基线、ADR 和 ContractVersion 均保持技术候选原样；若范围扩大，不能按本次身份修复直接请求 Approve。
5. 在实际 review_head 重跑 structure／cpp14／diff／all，四份 evidence JSON 的 pr_identity.head_sha 均须等于该提交，保存命令、退出码、诊断、工具版本及输入指纹。不能复制技术候选的旧数字。
6. PR 正文记录固定的 contract_candidate_sha 与实际 review_head，以及当前 HEAD 的真实检查结果；tracked 文档不再为追写自身 SHA 产生第二个提交。
7. R 的最终 Formal Review 必须绑定 GitHub 当前 HEAD，记录平台 Review URL；Conversation comment 不代替 Approval。

重跑命令均使用 `python tools/gate0/check_contract.py --layer <structure|cpp14|diff|all> --base-ref origin/main`。历史 7/7、8/8、1/1、15/15 只有在实际新提交复跑一致时，才可写成该 HEAD 的结果。原始资料指纹及未验证层仍须同步核对；完整业务实现责任保持[现有 D3 强制表](../baseline/01_导入Profile冻结说明.md)，不在本轮重新打开技术返工。

若 R 判断候选可合并，APPROVE 正文仍应明确“PR #2 候选通过 ≠ Gate 0 通过，Gate 0 等待 A/B/C/甲方及剩余基线条件”。Review 不是创建者的合并授权。

C-G0-01／02／03 是 Gate 0 剩余条件，不是该 Formal Review 新发现的代码缺陷，也不直接阻塞本次证据身份修复。R 是否 APPROVE 以新 HEAD 的实际复核为准；PR APPROVE／合并不等于 Gate 0 PASS，不自动允许进入 D2。

### A／B 与后续责任

A 仍需给出第二份样表／脱敏样本、重复候选识别与人工处置、性别／类别／级别和党员代码、Profile 唯一匹配、缺状态源业务选择、工号与固定编号关系的可审查基线。

B 的字段分类、旧 CareFlags／TagCodes、导入 revision 流程、系统字段只读、日期精度、模板来源、snapshot_id、旧 Q 项及 MD／HTML 证据返工继续归入 #3。#2 未经授权合并前不替 B 宣布依赖已就绪；不重建该阶段 PR，也不在本地合并分支。

Gate 0 仍未通过，见[Gate Status](GATE_STATUS.md)。R02 服务验收留 D3，完整 FilterSpec／快照与业务规则留 D4，GDI／xlsx 与输出对账留 D5；本轮只关闭可在公共契约层验证的风险。
