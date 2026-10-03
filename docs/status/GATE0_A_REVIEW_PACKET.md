# Gate 0 · A 轨审查包（D1 数据边界冻结 · Q1-B／Q2-A 落地）

面向非作者 R 的最小可执行审查包。**本文件不给出 Gate 结论**；结论只能由正式承担 R 角色且不是本变更作者的人填写，见 [Gate 状态](GATE_STATUS.md)。

| 项 | 值 |
| --- | --- |
| 阶段／轨道 | D1 / Gate 0 / A（数据与业务）；PR #6 分支 `docs/d1a-data-boundary-freeze` |
| 任务卡来源 | `reference/七阶段开发任务清单.xlsx` 施工台账 D1 / Gate 0 / A 行 |
| 本轮性质 | **Owner Decision 落地收口**（Q1-B + Q2-A），不是新开发任务 |
| 送审状态（A 轨自评） | `READY_FOR_BASELINE_INTEGRATION = YES`；`READY_FOR_FINAL_R_REVIEW = NO`（Q1-B／Q2-A 业务收口完成，但 #6 尚未纳入 PR #8 之后的 SP1 当前 main 基线） |
| Gate 0 未回答人类决定 | **0**（A-D1 TRUE BLOCKERS = 0） |
| 已登记口径（无需决策） | A-D1-06 四个标识符概念；不修改契约、不做破坏性迁移 |
| 仍留 D3／D4 | D3 九项、D4 一项（`AUTO_PINYIN_GENERATION_DEFERRED`） |
| 其它 | Risk 三项、TD 一项、Unknown 一项、跨轨观察一项 |
| 公共契约 | **未修改**（ContractVersion 4，Draft）；无新增依赖 |
| 变更形态 | 本轮只改已提交的 4 份材料与 1 处工具标签；公共契约、其它轨道文件与原始资料未改 |

## 1. 已落地的 Owner Decision（不再是问题）

| 决定 | 内容 | 来源 |
| --- | --- | --- |
| **Q1-B** | 首期业务工作簿数量 = **1**（`NO_SECOND_BUSINESS_WORKBOOK`）；唯一业务工作簿为 `reference/员工信息表11111.xlsx` | Owner Decision（2026-10-03 创建者直接回答）；当前 tracked 权威记录见 `docs/status/SP1_BASELINE_HANDOFF.md` 与 `docs/status/GATE0_REVIEW_HANDOFF.md`，平台记录见 [PR #8](https://github.com/gaoyizhe934/retiree-roster-win7/pull/8)。OD-0002 只承载 SP1 目标 OS 条款，不是 Q1／Q2 的业务授权来源 |
| **Q2-A** | `Sheet1` 的两套表头体系都是首期 Source Profile（`BOTH_SOURCE_PROFILES`）：**P1** = `sheet1-row1-v1`（行 1，52 标题）、**P2** = `sheet1-row3-v1`（行 3，23 标题） | 同上 |

本分支基线早于 PR #8 的合并，因此以上记录以 GitHub URL 与反引号路径引用，**不建立本地链接**（避免指向本分支不存在的文件）；main 到 #6 的基线整合按 `docs/status/SP1_BASELINE_HANDOFF.md` 通过 GitHub PR 安排，本轮不做本地 merge／rebase／pull。**在 #6 完成 SP1 基线整合前，本包只支持基线整合评审，不构成最终 Gate 0 Formal Review 的送审对象。**

### Q1-B 的边界

Q1 只确认**首期业务工作簿数量**，不声称世界上不存在其他文件，也**不推导** Q2。不得由“只有一个工作簿”得出“行 1 不是导入源”或“行 3 才是标准源”。

### Q2-A 的边界

两套 Profile **都属首期支持范围、互不覆盖、分别匹配、分别预检、各自拥有 mapping／profile version**；canonical Person 由两者共享：

```text
P1 ─┐
    ├→ canonical mapping → Person
P2 ─┘
```

**Source Profile ≠ Domain Model**：Profile 地位确认**不等于**映射、值域与导入策略已批准。不得把两套表头拼成一个超级 Profile，不得因字段同名跨 Profile 静默补值，不得把其中一套静默降级为历史区域。

## 2. 四份材料与决定的一致性

| 材料 | 落地内容 |
| --- | --- |
| [06_数据字典v1.md](../baseline/06_数据字典v1.md) | 新增「首期业务数据源与 Source Profile」节：1 个工作簿 + P1／P2 表；Person 字典改为「源覆盖（P1 / P2）」；无源字段缺口按 P1／P2 重述；删除“第二份工作簿缺失”“区域 1 是否为导入源尚未确认”等已被决定解决的表述 |
| [07_源表字段映射.md](../baseline/07_源表字段映射.md) | 新增「Source Profile 层」节：P1／P2 标识、位置描述、约束与关系图；五个 `Unsupported` 改述为“有效 Source Profile 中尚未获得安全 canonical 映射的列”；P2 节改为跨 Profile 关系；同义表按 P1／P2 标注 |
| [09_D1A未决项清单.md](../baseline/09_D1A未决项清单.md) | A-D1-01／A-D1-07 → `CLOSED_OWNER_DECISION`（保留历史问题与决定来源，记录六项共同影响）；新增该分类；**A-D1 TRUE BLOCKERS = 0、未回答人类决定 = 0**；P1 映射细节归入 A-D1-04（D3） |
| 本审查包 | 决策表 → 落地核对表；审查步骤改为核验决定是否正确落地 |

`NO_SECOND_BUSINESS_WORKBOOK` 与 `BOTH_SOURCE_PROFILES` 在四份材料中的含义一致：业务工作簿数量 = 1，两套 Source Profile 都受支持。

## 3. R 应重点复核（Q1-B／Q2-A 是否被正确落地）

| # | 复核点 | 期望 |
| --- | --- | --- |
| 1 | 两个 Profile 是否**独立表达** | 06／07 各有 P1、P2 的独立条目与标识；没有合并的超级 Profile |
| 2 | 52／23 字段盘点是否**完整** | P1 = 52 个非空标题（20 `PersonField`／27 `BatchRawOnly`／5 `Unsupported`）；P2 = 23 列全部 `PersonField`；合计 75，无静默丢弃 |
| 3 | mapping 是否**没有跨 Profile 静默补值** | 07 明示“不因字段同名跨 Profile 补值、不拼超级 Profile”；同义表只作人工确认依据 |
| 4 | `Unsupported` 是否**未被静默吞掉** | A、G、H、AW、AY 五列仍为 `Unsupported`，仍按“预检发现 → 显式展示 → 阻断确认／人工处置”处理；Q2-A 未把它们升级为 `BatchRawOnly` |
| 5 | Deferred 项是否**没有被错误宣告解决** | 8 个无同名键可比对的目标、P2 值域、Tag 值域、判重分档、Tag 唯一键仍在 D3；A-D1-10 仍在 D4；A-D1-17 等仍在 Risk |
| 6 | **HEADER-ONLY 限制是否仍在** | 06／07／09 均保留“0 数据行、数据级结论 UNKNOWN”；A-D1-02 仍为 D3 |
| 7 | 决定来源与历史是否保留 | A-D1-01／A-D1-07 保留原问题文字与决定来源；未删除历史条目、未重排编号（A-D1-01…19） |

## 4. R 执行步骤

| # | 步骤 | 命令／文件 | 期望 |
| --- | --- | --- | --- |
| 1 | 验证原始 Excel 指纹与 HEADER-ONLY 事实 | `python tools/d1a/inventory_d1a.py` | 退出 0；SHA-256 `427727f5…2cf5b6`；`Sheet1`、`A1:IS3`；非空行 `[1, 3]`（52／23）；`数据行: 0 行 -> HEADER_ONLY_SAMPLE` |
| 2 | 核对两个 Profile 的机器可读声明 | 同上的「表头区域」段 | 打印 `区域 1 / Source Profile P1（sheet1-row1-v1）` 与 `区域 2 / Source Profile P2（sheet1-row3-v1）`，表头行为 1／3 |
| 3 | 审阅 P1 逐列分类（52） | [01-source-header-inventory.txt](../evidence/D1-A/01-source-header-inventory.txt)、[07_源表字段映射.md](../baseline/07_源表字段映射.md) | 20／27／5；空标题列 I、M、AS、AU、AV、AX、AZ–BC 保留位置 |
| 4 | 审阅 P2 逐列分类（23） | [02_字段映射与数据保留策略.md](../baseline/02_字段映射与数据保留策略.md)、同一证据 | 23 列全部映射，目标互不重复；W 为空标题列 |
| 5 | 审阅五个 `Unsupported` | [07_源表字段映射.md](../baseline/07_源表字段映射.md) | A、G、H、AW、AY 仍是 `Unsupported`，语义为“有效 Profile 中尚未获得安全 canonical 映射的列”，不静默丢弃、不擅自映射、不创造字段 |
| 6 | 审阅 8 个机器不可核验目标 | 同上「输入身份与机器可读声明」段 | P 手机、X 离退休时间、Z 类别、AD 所属支部、AF 原部门、AP 人员状态、AQ 转正日期、AT 现学历 仍待人工复核（D3） |
| 7 | 审阅重复候选规则 | [08_重复候选规则草案.md](../baseline/08_重复候选规则草案.md) | 双作用域、不做模糊匹配、任何候选阻断确认、DUP-01～12 未运行（D3 验收） |
| 8 | 审阅重分类后的未决项 | [09_D1A未决项清单.md](../baseline/09_D1A未决项清单.md) | 2 项 `CLOSED_OWNER_DECISION`、0 项 Gate 0、1 项已登记口径、9 项 D3、1 项 D4、3 项 Risk、1 项 TD、1 项 Unknown、1 项跨轨 |
| 9 | 执行 L0 检查器与证据新鲜度 | `python tests/contract/check_d1a_regressions.py --log docs/evidence/D1-A/02-checker-regression.txt` | 退出 0；14 行 PASS（12 项漂移必失败 + 2 项证据逐字节校验） |
| 10 | 执行结构层（本分支） | `python tools/gate0/check_contract.py --layer structure` | **7/7、退出 0**（本分支不含 C 轨证据文件；A-D1-14 的空白缺陷只在含 C 证据的分支出现） |
| 11 | 给出结论 | 见下方四选一 | **由 R 填写** |

## 5. R 的结论选项

| 结论 | 含义 |
| --- | --- |
| `PASS` | 决定落地与交付物均接受，无需延期登记 |
| `PASS_WITH_REGISTERED_DEFERRED_ITEMS` | 接受落地结果，D3／D4／Risk／TD／Unknown 各按其登记阶段跟踪 |
| `REWORK` | 落地存在需返工的问题（请指出编号或文件行） |
| `BLOCKED` | 因外部资料或跨轨条件无法形成可信基线 |

A 轨不代签；Q1-B／Q2-A 已决定，不再作为待答问题出现。

## 6. 轨道边界（A 本轮未做也不应做的事）

- 未修改 C 轨证据、`tools/gate0/check_contract.py`、`.gitattributes`、C 的构建文件、CMake／XMake 定义。
- 未修改公共契约、`docs/baseline/00–05`、`docs/decisions/*`、`docs/status/GATE_STATUS.md`、四份带指纹的原始资料。
- 未做本地 merge／rebase／pull，未生成合并提交；未执行任何 Git 写操作（无 add／commit／push／PR／merge／分支创建）。
- 未新增产品代码、数据库、界面或 GDI 打印代码；未实现 xlsxio_read 导入或规则引擎；未引入任何新依赖。
- 未运行 L1／L2／L3，未在 Win7 验证。目标 OS 基线已由 **OD-0002（仅限目标 OS 条款）** 修订为 Windows 7 SP1 / 6.1.7601；本包不重述 OS 条款，也不主张任何 Win7 证据（历史证据中的 RTM 表述属当时环境）。

## 7. Git 材料（仅准备）

- 分支：`docs/d1a-data-boundary-freeze`（PR #6，继续使用，不新开 A-D1 PR）
- 建议提交标题：`docs: 落地Q1-B与Q2-A数据边界Owner Decision`
- 建议提交正文要点：四份材料一致反映 `NO_SECOND_BUSINESS_WORKBOOK` 与 `BOTH_SOURCE_PROFILES`；A-D1-01／A-D1-07 关闭并保留历史；A-D1 TRUE BLOCKERS = 0；契约未改；证据由工具重新生成。
- 基线说明：本分支基于 `567d9cd`，早于 PR #8 的 SP1 合并；main → #6 的基线整合按 `docs/status/SP1_BASELINE_HANDOFF.md` 通过 GitHub PR 安排，不使用本地 merge／rebase／pull。
- PR 正文草稿：`build/d1a/pr-body-draft.md`（本地待同步材料，位于被忽略目录）
