# Gate 0 · A 轨审查包（D1 数据边界冻结）

面向非作者 R 的最小可执行审查包。**本文件不给出 Gate 结论**；结论只能由正式承担 R 角色且不是本变更作者的人填写，见 [Gate 状态](GATE_STATUS.md)。

| 项 | 值 |
| --- | --- |
| 阶段／轨道 | D1 / Gate 0 / A（数据与业务） |
| 任务卡来源 | `reference/七阶段开发任务清单.xlsx` 施工台账 D1 / Gate 0 / A 行 |
| 送审状态（A 轨自评） | **可送审**：三项交付物 + 未决项登记 + L0 证据 + 漂移回归齐备 |
| Gate 0 人类决策 | **2 项**（Q1 业务工作簿数量；Q2 两套表头体系的性质） |
| 已登记口径（无需决策） | A-D1-06 四个标识符概念；不修改契约、不做破坏性迁移 |
| 不阻塞 D2 的延期项 | D3 九项、D4 一项（`AUTO_PINYIN_GENERATION_DEFERRED`） |
| 其它 | Risk 三项、TD 一项、Unknown 一项、跨轨观察一项 |
| 公共契约 | **未修改**（ContractVersion 4，Draft）；无新增依赖 |
| 变更形态 | 纯新增 10 个文件；`git diff` 对已跟踪文件为空 |

## 1. 送审交付物

| 交付物 | 文件 |
| --- | --- |
| 数据字典 v1（Person／Tag／ImportBatch／PrintTemplate） | [06_数据字典v1.md](../baseline/06_数据字典v1.md) |
| 源表映射表（两套表头的逐列处置） | [07_源表字段映射.md](../baseline/07_源表字段映射.md) |
| 重复候选规则草案 | [08_重复候选规则草案.md](../baseline/08_重复候选规则草案.md) |
| 未决项与 Gate 0 分类清单 | [09_D1A未决项清单.md](../baseline/09_D1A未决项清单.md) |
| L0 盘点证据 / 漂移回归日志 | [01-source-header-inventory.txt](../evidence/D1-A/01-source-header-inventory.txt)、[02-checker-regression.txt](../evidence/D1-A/02-checker-regression.txt) |
| 检查器与回归 | [inventory_d1a.py](../../tools/d1a/inventory_d1a.py)、[check_d1a_regressions.py](../../tests/contract/check_d1a_regressions.py)、[工具说明](../../tools/d1a/README.md) |

A 轨**不主张**：任何数据级统计（无数据行）、任何 Gate 结论、任何 L1/L2/L3 或 Win7 证据、任何产品代码（仓库仍无 `src/`）。

## 2. 人类决策表（Gate 0 只需回答这 2 项）

### Q1 — 首期是否还有第二份独立业务工作簿？

- **为什么现在必须回答**：Gate 0 即数据边界冻结；台账 D1-A 要求盘点两份 Excel。字段字典的完整性在缺少一份可能存在的业务源时无法被审查。**本项只回答业务文件数量**，不得用于推导任何表头体系的地位（那由 Q2 决定）。
- **已验证事实**：项目目录 `D:\retiree-roster`（含 `tools\`，排除 `.git`）全量扫描 `*.xlsx/*.xls/*.xlsm` 只有两份文件——业务样表 `员工信息表11111.xlsx` 与项目管理台账 `七阶段开发任务清单.xlsx`（台账四个工作表均为管理台账，不是业务数据源）。
- **OPTIONS**
  - **A**：存在第二份独立业务工作簿，稍后补充（请附无个人数据的表头样本）。
  - **B**：不存在，首期只有当前这一份业务工作簿。
- **RECOMMENDED**：**A 轨不代选。** 按指令，本项由 R／甲方选择；A 轨只登记影响范围。
- **IMPACT**：A → 字段覆盖需重评，可能出现新的 canonical 字段（契约变更 + 迁移），本审查包的字段部分需重做；B → 业务源数量确认为 1，字段覆盖结论的输入范围确定，但**行 1／行 3 的地位仍由 Q2 决定**。
- **DEFAULT IF DEFERRED**：本项属数据边界，**不允许延期**；未回答前 Gate 0 无法冻结、D2 不得开始。

### Q2 — 当前 Sheet1 的两套表头体系是什么关系？

- **为什么现在必须回答**：行 1（52 个非空标题）与行 3（23 个非空标题）是两套明显不同的字段体系；行 1 内部还分成业务维护段、姓名一致性标记列、人事对照段与待遇／考核段；两区域有 12 个完全同名标题、6 组行 1 内部精确重复标题。在两套体系的地位确认前，**源字段映射边界没有真正冻结**——既不能断言哪一套是首期导入源，也不能断言另一套是历史结构。
- **已验证事实**：两套表头的列集合、规范化键、重复键、跨区域同名键、合并单元格与受保护区域均已逐字节盘点并机器校验；行 1 的 52 列已全部给出候选处置（20 `PersonField`／27 `BatchRawOnly`／5 `Unsupported`），行 3 的 23 列沿用既有候选映射；数据行为 0。两套表头都有实际业务列：行 1 有人员状态、类别、社保卡手机号、分区／楼号、特困年度等，行 3 有学历、学位、入党时间、籍贯等。
- **OPTIONS**
  - **A**：两套都是首期需要支持的 Source Profile。
  - **B**：行 1 有效，行 3 为历史或辅助结构。
  - **C**：行 3 有效，行 1 为历史或辅助结构。
  - **D**：其他，由甲方说明。
- **RECOMMENDED**：**A**。理由：两套结构都有实际业务列，在无业务证据时宣告任一套为“历史结构”会丢源；A 对“实际维护哪一套”这一未知不做假设，且两区域各自的映射已分别登记（区域内无重复目标）。
- **IMPACT**：A → 需要两个 Profile；行 1 的映射细节（哪个电话列映射 `Phone`、`现居地` 是否等同 `HomeAddress`、业务段与人事段在重复列上的权威顺序）在 D3 逐项确认；行 1 的 5 个 `Unsupported` 列按现行策略阻断确认，需维护员逐批处置。B → 行 1 封存为非导入结构，其人员状态、类别、特困等列失去导入路径，`LifeStatus`／`PersonnelCategory` 首期无导入来源。C → 行 3 封存，需为行 1 新建完整 Profile 并重评 8 个无同名键可比对的目标。D → 按甲方说明重新评估映射表与 Profile 候选。
- **DEFAULT IF DEFERRED**：**不允许延期**（源字段映射边界未冻结）。若甲方要求先推进，只能按 A 的保守口径**记录**（两套都列为候选 Profile、都不视为已批准），且 Gate 0 不得宣告冻结。

## 3. 已登记口径（不需要人类决策）

### A-D1-06 四个标识符概念

| 概念 | 契约成员 | 性质 |
| --- | --- | --- |
| 内部主键 | `person_id` | 系统生成、不复用；不可导入、不可编辑、系统专管、不打印 |
| 源工号 | `employee_no` | 来自源表“工号”列；可导入、可编辑、可打印，可空可重复 |
| 固定业务编号 | `person_code` | 不可导入、不可编辑、系统专管、可打印；**只能由服务分配** |
| 当次序号 | `RosterRow.print_serial_number`（`DerivedColumnId::PrintSerialNumber`） | 每次生成时按当前筛选结果从 1 连续派生，**不持久化** |

**结论：现有冻结契约已支持该模型，无需契约变更、无需破坏性迁移。** 依据：`person_code` 的 `source_importable=false, user_editable=false, system_managed=true`；`ImportFieldId` 与 `EditableFieldId` 均不含 `PersonId`／`PersonCode`；`is_valid_import_binding`／`is_valid_field_change` 拒绝系统专管与 Identifier 目标 → 结构上不可能出现“两个可写的固定编号来源”（这正是[编号口径](../baseline/03_标识符与编号口径.md)当初提出撤销 `PersonCode` 所防的情形）。

若甲方未来确认源工号与固定编号同义，采用**映射同值**而非删除字段：服务在创建时一次性快照赋值，创建后改工号不改变固定编号；工号为空或重复时回退到系统分配的不复用编号（回退规则由甲方确认）；格式变化不影响契约（`Identifier` 为文本）。

待 R 认可的两处**文字口径**（非结构问题）：[字段映射与数据保留策略](../baseline/02_字段映射与数据保留策略.md) 的“系统分配……不从源表映射”理解为“不从源表列映射”；[编号口径](../baseline/03_标识符与编号口径.md) 的“若等同则撤销 PersonCode”在当前契约下已无必要。两份文档本轮均未修改。

## 4. R 审查步骤（按顺序执行）

| # | 步骤 | 命令／文件 | 期望与关注点 |
| --- | --- | --- | --- |
| 1 | 验证原始 Excel 指纹与 HEADER-ONLY 事实 | `python tools/d1a/inventory_d1a.py` | 退出 0；SHA-256 `427727f5…2cf5b6`；工作表 `Sheet1`、维度 `A1:IS3`；非空行 `[1, 3]`（52／23 个标题）；`数据行: 0 行 -> HEADER_ONLY_SAMPLE` |
| 2 | 审阅两套表头的逐列分类 | [01-source-header-inventory.txt](../evidence/D1-A/01-source-header-inventory.txt)、[07_源表字段映射.md](../baseline/07_源表字段映射.md) | 行 1 的 52 个非空标题逐列有处置；空标题列 I、M、AS、AU、AV、AX、AZ–BC 保留物理位置。关注是否有静默丢弃 |
| 3 | 审阅 PersonField / BatchRawOnly / Unsupported 划分 | [07_源表字段映射.md](../baseline/07_源表字段映射.md) | 行 1：20／27／5，合计 52；5 个 `Unsupported` 是 A `bi`、G 身份证提取出生年、H 身份证2026年 年龄、AW 现考核、AY 现执行工资；行 3：23 列全部 `PersonField`。关注 `Unsupported` 会阻断确认 |
| 4 | 审阅重复标题映射一致性 | [07_源表字段映射.md](../baseline/07_源表字段映射.md) | 6 组行 1 精确重复键各只有一列成为 canonical 目标；4 组逐字节同名（D/AJ、E/AK、AC/AO、T/U），2 组仅空白不同（C/AI、F/AN） |
| 5 | 审阅无同名源字段的 8 个目标 | 同上「输入身份与机器可读声明」段 | 机器只验证合法性与唯一性；P 手机、X 离退休时间、Z 类别、AD 所属支部、AF 原部门、AP 人员状态、AQ 转正日期、AT 现学历 需人工判断语义 |
| 6 | 审阅重复候选规则 | [08_重复候选规则草案.md](../baseline/08_重复候选规则草案.md) | 批内／批间双作用域、不做模糊匹配、任何候选阻断确认、四种人工处置、DUP-01～12 未运行（属 D3 验收） |
| 7 | 审阅重新分类后的未决项 | [09_D1A未决项清单.md](../baseline/09_D1A未决项清单.md) | 2 项 Gate 0（A-D1-01 文件数量、A-D1-07 表头体系性质）、1 项已登记口径（A-D1-06）、9 项 D3、1 项 D4、3 项 Risk、1 项 TD、1 项 Unknown、1 项跨轨；关注分类判据是否被一致应用 |
| 8 | 执行 L0 检查器 | `python tests/contract/check_d1a_regressions.py --log docs/evidence/D1-A/02-checker-regression.txt` | 退出 0；14 行 PASS（12 项漂移必失败 + 2 项证据新鲜度）。关注证据是否被手工改过（会失败） |
| 9 | 执行漂移回归（独立复跑） | `python tools/d1a/inventory_d1a.py --evidence-dir docs/evidence/D1-A` 后重跑步骤 8 | 退出 0；证据逐字节不变。可选：`python tools/gate0/check_contract.py --layer structure`（当前 6/7，唯一失败为 C 轨证据空白，见 [A-D1-14](../baseline/09_D1A未决项清单.md)） |
| 10 | 给出结论 | 见下方四选一 | **由 R 填写**，本文件不预设结论 |

## 5. R 的结论选项

| 结论 | 含义 |
| --- | --- |
| `PASS` | 交付物与分类均接受，无需延期登记即可冻结 A 轨数据边界 |
| `PASS_WITH_REGISTERED_DEFERRED_ITEMS` | 接受 A 轨数据边界，D3／D4／Risk／TD／Unknown 各按其登记阶段跟踪 |
| `REWORK` | 交付物存在需返工的问题（请指出编号或文件行） |
| `BLOCKED` | 因人类决策、外部资料或跨轨条件无法形成可信基线 |

无论哪种结论，**A 轨都不代签**；Q1 或 Q2 未回答时 Gate 0 无法冻结（业务源数量或源字段映射边界不完整）。

## 6. 轨道边界（A 本轮未做也不应做的事）

- 未修改 C 轨证据、`tools/gate0/check_contract.py`、`.gitattributes`、C 的构建文件、CMake／XMake 定义。
- 未修改公共契约、`docs/baseline/00–05`、`docs/decisions/*`、`docs/status/GATE_STATUS.md`、四份带指纹的原始资料。
- 未新增产品代码、数据库、界面或 GDI 打印代码；未运行 L1／L2／L3；未在 Win7 验证。
- 未执行任何 Git 写操作（无 add／commit／push／PR／merge／分支创建）。

## 7. Git 材料（仅准备）

- 分支：`docs/d1a-data-boundary-freeze`（从 `origin/main` `567d9cd` 切出；`git check-ref-format --branch` 已通过）
- 提交标题：`docs: 交付A轨D1数据字典、源表映射与重复候选规则`
- PR 标题：`docs: 交付A轨D1数据字典、源表映射与重复候选规则`（正文首行 `阶段/轨道：D1 / Gate 0 / A`）
- PR 正文草稿：`build/d1a/pr-body-draft.md`（本地待同步材料，位于被忽略目录）
