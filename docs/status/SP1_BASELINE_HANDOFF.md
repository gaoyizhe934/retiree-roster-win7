# Windows 7 SP1 基线修订与跨轨交接

Windows 7 SP1 基线修订由 [PR #8](https://github.com/gaoyizhe934/retiree-roster-win7/pull/8) 承载，包括 [OD-0002](../decisions/OD-0002-Windows7-SP1目标基线.md)、三份受控资料修订、指纹及入口/状态统一。修订前基线锚点为 `567d9cd32befc2b8aa7ae99487f8b6d2170f1436`，仅用于复核 v2.0 → v2.1 的固定差异，不是“当前 main”声明。

PR #8 的当前 HEAD、Review 与合并状态以 GitHub 平台记录为准；tracked 文档不追写自身或其它阶段 PR 的当前 HEAD。固定内容身份与完整差异见 [OOXML 语义证据](../evidence/D1-SP1/01_受控基线OOXML语义差异.md)。

## 阶段 PR 与纳入要求

| 轨道 | 承载 PR | SP1 纳入要求 | 后续验收 |
| --- | --- | --- | --- |
| A | [#6](https://github.com/gaoyizhe934/retiree-roster-win7/pull/6) | 按 Q1-B/Q2-A 同步 06/07/09/Review Packet；按单一来源同步基线指纹 | A L0、回归及对应候选的 R 复核；五个 Unsupported 和八个语义项继续 D3 |
| B | [#3](https://github.com/gaoyizhe934/retiree-roster-win7/pull/3) | 在阶段 PR 纳入 SP1 基线时更新设计正文的当前性 RTM 条款、交付记录，重建 MD/HTML/JSON | build_design.py --check、test_build_design.py、对应候选的 Formal Review |
| C | [#7](https://github.com/gaoyizhe934/retiree-roster-win7/pull/7) | 在阶段 PR 纳入 SP1 基线时于 VM 完成说明及接手记录引用 OD-0002，提供可追溯 Guest/工具链/交接来源与链接证据 | Guest 版本及纯净性、正式工具链和交接证据的 R 复核 |

各阶段 PR 在最终 Gate 0 复核前必须完成自身的基线同步与验收；是否完成以各 PR 的 GitHub Diff / Review 为准。本基线 PR 的范围由 OD-0002 与固定二进制差异界定；阶段交付和返工分别沿 #3/#6/#7 处理，维持每阶段一个有效 PR。

所有分支整合通过 GitHub PR；每次合并都须用户明确授权及必要评审。不能本地 merge/rebase；同步已合并的线性内容仅使用 `git pull --ff-only`。若现有阶段分支不能快进，保留现场，通过 GitHub PR 安排 main 到该阶段分支的基线整合，而不强推或重建阶段 PR。集成 PR 只运送基线，不替代阶段成果 PR。

## 已取得的 A 人类决定

来源为本任务 2026-10-03 的直接回答：

> Q1-B：确认首期只有这一份
>
> Q2-A：两套都作为首期 Source Profile（清单建议）

Q1 是首期业务范围确认，不声称世界上不存在其他文件，也不推导 Q2。Q2 分别使用 P1（Sheet1 行1、52 标题）与 P2（行3、23 标题）；保留物理区域及全部列处置，0 数据行事实不变。五个 Unsupported 和八个机器不能核验的映射语义留 D3；Profile 地位确认不等于映射、值域和导入策略已批准。

A 的 06/07/09/Review Packet 必须一致：NO_SECOND_BUSINESS_WORKBOOK、BOTH_SOURCE_PROFILES，未回答人类决定为 0。这些是 Owner/业务决策事实；#6 是否已同步完成，以 #6 GitHub Diff / Review 为准。A 阶段复跑：

```text
python tools/d1a/inventory_d1a.py --evidence-dir docs/evidence/D1-A
python tests/contract/check_d1a_regressions.py --log docs/evidence/D1-A/02-checker-regression.txt
```

OD-0002 修订了任务台账指纹，A/B 检查器若另有硬编码或生成输入指纹，须按其单一来源同步；业务样表指纹保持不变，各阶段证据须使用实际输入重新生成。

## C 证据边界

VM 名称 Win7RTM-SP1-x86/x64 是实际机器的历史命名，不手改 VBoxManage 原始输出。OD-0002 仅决定目标 OS 条款；Guest 系统版本、已安装程序、纯净性与正式工具链必须由真实证据和 R 复核确认。截图采集、交接来源及链接由 C 在 #7 提供并交 R 检查，不能由说明文字或本基线 PR 的 Review 代替。

## 检查与审查身份规则

```text
python tools/gate0/check_contract.py --layer structure --base-ref origin/main
python tools/gate0/check_contract.py --layer cpp14 --base-ref origin/main
python tools/gate0/check_contract.py --layer diff --base-ref origin/main
python tools/gate0/check_contract.py --layer all --base-ref origin/main
```

每次新增提交后在该实际 HEAD 复跑四层检查，由 PR #8 正文及 Formal Review 绑定 review_head、base、merge-base、输入指纹与真实检查结果。未提交候选由输入指纹标识；这种通用检查规则不声明任何候选的发布状态。本地 JSON 与渲染 QA 使用忽略目录 build/gate0/sp1；可独立复核的固定二进制差异保存在上述 tracked OOXML 证据中。作者检查不代替 Formal Review，不证明 Win7 L2/L3 或 Gate 0 PASS。
