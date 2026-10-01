# PR #2 返工与人工审核报告

日期：2026-10-01。依据《2PR_自我审查与返工清单》继续原 #2 分支，本轮不新建 PR，不实现 D2 产品功能。

返工审核时的远端 HEAD：`bc04290224ee2ba43b3026f1787d1e1c8f16a37f`。
PR base：main `af0ae01981ac3d65653921ceada1cee605de5607`。
工作分支：`fix/gate0-baseline-stabilization`。
以下记录该 HEAD 之上的返工审核候选；源文件指纹标识当时的未提交候选，不能把上述 HEAD 称为本轮修改后的提交。创建者随后明确授权“commit,push,prbody”；发布后的提交身份及重新运行的检查结果记录在 PR #2 正文。

## 清单逐项处理

| 条目 | 本轮处理 | 当前状态 |
| --- | --- | --- |
| P0-01 分支规则来源 | 保留创建者此前直接要求的 ASCII；OD-0001 引用原话，明确只覆盖分支命名；不采用附件相反建议 | 来源已补齐，规则未撤销 |
| P0-02 Gate 权限 | Gate 质量结论仅由正式承担评审角色的非作者 R 签认；Git 授权独立，作者不能切换身份自签 | 已修改 |
| P0-03 预检确认 | Confirm 仅收 batch_id、preview_revision、confirmed_by 与元信息；预检输出含 revision／源指纹，批次追溯同 revision | DTO 已修改；D3 服务行为仍待实现 |
| P0-04 系统字段写入口 | PersonCreateInput／PersonEditInput／TagMutation 分离；类型化导入／编辑字段，能力元数据与强转校验 | 已修改，编译及行为检查通过 |
| P1-01 导出路径 | 私有 ExportLogRecord 保存真实 output_path；UI／公开证据另行脱敏 | 已修改 |
| P1-02 PR Diff 检查 | 解析 base/head/merge-base，检查已提交 PR、暂存与工作区；记录命令／退出／诊断 | 已修改，隔离回归通过 |
| P1-03 本机历史 | 从长期 baseline 移除，现场仅记录在本报告 | 已修改 |
| P2-01 检查工具链 | all／structure／cpp14／diff 分层，未执行层明确记录 | 已修改 |
| P2-02 Profile 冻结 | 移除可写 frozen 布尔值，批准状态从配置仓储／审批记录取得 | 模型已修改，仓储实现待 D3 |
| P2-03 版本命名 | ContractVersion／contract_version 与 DatabaseSchemaVersion 分离，契约草案修订为 3 | 已修改 |

P0-01 的审查前提与创建者原始指令不符；决定来源及精确引用见 [OD-0001](../decisions/OD-0001-分支命名规则.md)。此处不把代理选择描述为新的批准决定。其余四份 ADR 仍为 Proposed，Gate 0 未通过。

## 公共输入与保存对象

创建仅接收业务字段，服务分配 PersonId／PersonCode、初始化拼音并生成审计。编辑目标不包含系统专管字段；PinyinSortKey 不可导入但允许创建后的人工编辑。源状态列必须显式确认映射并解析有效值。系统 ID、固定编号及四个审计字段的 source_importable／user_editable 均为 false，system_managed 为 true。

标签修改不接收 updated_at／updated_by，服务根据操作上下文与系统时间统一生成。Confirm 不再允许提交状态或映射参数，所有映射、Profile、状态、重复处置、文件内容／工作表变化均需新 revision 及重新预检；确认只能读取服务保存的该次不可变结果。事务、重复执行拒绝、缓存与源内容一致性仍须 D3 集成验证。

## 核心对象与未决口径

| 对象 | 与需求逐字段对照 | 未决／后续验证 |
| --- | --- | --- |
| ImportBatchRecord | 批次、源文件名、工作表、源／有效／导入／异常数、重复候选数、执行时间；补 revision、源指纹、映射／Profile 版本与状态来源 | 实际批次写入与查询待 D3/D6 |
| PrintTemplate | 字段／列序／列宽、正文／标题／表头字号、A4、方向、四边距、行高、每页人数、签字列、重复表头／页码 | 构造默认是建议值；甲方模板参数及 GDI/xlsx 转换待确认验证 |
| ExportLogRecord | 模板／版本、脱敏条件摘要、人数、真实输出路径、时间；补快照、归属、结果 | 本机私有数据库保存路径，公开展示脱敏；持久化与输出对账待 D5/D6 |

未写死的 D1A/B/C/R 事项：固定编号格式与工号等价、无状态源时的业务选择、第二份样表、重复候选／枚举与党员代码、Profile 匹配、模板参数、固定依赖 notice、正式构建与双 Win7 RTM 基线。R 的正式非作者签认尚未提供。#1 保持后续 S4 返工依赖，不在本轮改动。

## 逐文件修改原因

| 文件 | 原因 |
| --- | --- |
| include/retiree_roster/schema_types.hpp | revision 确认、受限业务输入／字段能力、Tag 审计归一、真实导出路径、去冻结布尔与版本命名 |
| tests/contract/preview_revision_test.cpp | 验证确认绑定 revision 且不能提交状态决策 |
| tests/contract/input_authority_test.cpp | 验证输入无系统／审计字段、类型限制及强转伪造拒绝、显式状态源 |
| tests/contract/check_tool_regressions.py | 隔离 Git 历史复现 clean 工作区中的 PR 空白缺陷及 base 解析 |
| tests/contract/consumer_contract_test.cpp | 对齐新的 user_editable 能力元数据 |
| tools/gate0/check_contract.py | 真正覆盖 PR Diff、记录 base/head/命令、新增消费者／负例、分层执行 |
| tools/gate0/README.md | 分层命令、base 配置与证据边界 |
| docs/decisions/OD-0001-分支命名规则.md | 引用创建者直接指令，补命名决定证据 |
| GitHub协作命名规范.md | 指向可审查的命名决定 |
| CONTRIBUTING.md | 质量签认与 Git 授权分离，禁止作者角色切换自签 |
| .github/pull_request_template.md | Gate 结论仅非作者 R 填写，Git 授权独立 |
| docs/status/GATE_STATUS.md | 同步 R 权限和 ContractVersion 3，仍未通过 |
| docs/baseline/00_基线与权威来源.md | 来源引用、R 权限、移除本机历史 |
| docs/baseline/01_导入Profile冻结说明.md | revision、源内容绑定、批准记录与受限状态映射 |
| docs/baseline/02_字段映射与数据保留策略.md | 输入能力／审计、真实路径及脱敏层次 |
| docs/baseline/05_筛选与打印契约.md | 契约／数据库版本分离、候选默认参数不冒充冻结 |
| docs/decisions/ADR-0001-仓库基线权威顺序.md | R 质量签认独立于创建者 Git 授权 |
| docs/decisions/ADR-0003-名单快照与输出一致性.md | ExportLog 恢复需求中的真实输出路径 |
| docs/decisions/ADR-0004-标签与关怀状态模型.md | TagMutation 业务输入与服务生成审计 |
| docs/dependencies/THIRD_PARTY.md | 许可证质量签认由非作者 R 完成 |
| docs/status/STABILIZATION_REVIEW.md | 本轮逐项返工、实际证据与交接，不继承旧检查数字 |

## 验证

完整命令：`python tools/gate0/check_contract.py --base-ref origin/main`。整改后 12/12 通过、退出码 0；这是本轮新检查结果。无 MinGW 的任务子进程中 --layer structure 单独 7/7 通过，编译器记录为 not_executed，证据保存在被忽略的 build/gate0/structure-results.json。
已复现的 red：旧 Confirm 模型缺 revision 且可改状态，旧创建输入可写 ID／审计；旧检查脚本不能提供已提交 Diff 的身份／诊断证据。
修复后两个 C++ 消费者语法检查通过，隔离 Git 工具回归通过。

| 实际检查 | 结果 |
| --- | --- |
| 原始资料／源字段 | 四份基线指纹不变，23/23 源列映射覆盖 |
| 日期与通用消费者 | C++14 编译／执行成功，退出 0 |
| preview_revision | revision 输入可表达，Confirm 不含状态决策；编译／执行成功 |
| input_authority | 系统字段能力、强转伪造拒绝、状态源确认；编译／执行成功 |
| 编译负例 | 正常控制成功，21 个旧／越权消费者被明确编译拒绝 |
| R02 数据 | 13 条预期案例完整，未执行规则引擎 |
| Python 工具回归 | 已提交空白缺陷失败、修复成功、无效 base 失败、环境覆盖生效、不可执行编译器不被 Python 层启动 |
| 忽略／属性 | 12 个私有产物探针、6 个必要资源探针及 Word／Excel binary 验证通过 |
| 文档 | 18 份 Markdown 中 38 个本地链接有效 |
| PR Diff | base／merge-base 为 af0ae01981ac3d65653921ceada1cee605de5607，HEAD 为 bc04290224ee2ba43b3026f1787d1e1c8f16a37f；已提交 PR、暂存、工作区三条检查均退出 0 |

编译器为 MinGW GCC 6.3.0，以 -std=c++14 -Wall -Wextra -pedantic-errors 检查；不替代正式 MSVC 工具链。暂存区为空，本轮后续发布形成新 HEAD 时必须再核对实际 PR Diff 与提交证据。

检查 JSON 保存在被忽略的 build/gate0/results.json，包含执行层、工具版本、全部输入指纹；Diff 项保存 base SHA、head SHA、merge-base SHA及三条命令的结果。未提交修改以输入指纹标识。
原始四份 Word／Excel 未改；没有新增真实人员数据、数据库、备份、导出或运行日志。

未运行：正式 MSVC2017／CMake／XMake，SQLite 事务、年龄／党龄规则引擎、revision 确认服务、快照失效集成、GDI、xlsx、Win7 L2/L3 与物理打印。结构／编译检查不构成这些功能或 Gate 的通过证据。

## Standards

独立辅助审查发现 1 项 P2：Python 结构层仍采集 g++ 版本。已限制编译器调用为 all／cpp14，structure／diff 标记未执行，启动异常不阻止 JSON 保存；新增不可执行编译器回归，且真实无 MinGW 结构层运行通过。定向复核确认闭环；剩余发现 0。此辅助审查不代替正式非作者 R。

## Spec

独立辅助审查发现 0 项。输入权限、revision、Gate／Git 分离、真实路径、实际 PR Diff 和来源清理符合本轮范围；P0-01 按用户明确 ASCII 指令补来源。此辅助审查不代替 A/B/C/R 交叉复核或 Gate 签认。

本轮五项工作完成 5/5：来源／治理、输入契约、需求对照、验证、辅助审查与交接。完成指本地返工候选，不表示正式 Gate 或整份合并门槛完成。

## 本轮工作现场与发布

原有未跟踪 CONTEXT.md、docs/adr/、目录说明保留，不纳入本轮返工；这仅是本次现场记录，未来开发者无需在公共仓库寻找它们。

本轮继续 #2。创建者已在查看返工材料后明确授权 commit、push 和更新 PR 正文；按该授权发布本轮候选并更新正文，发布后的 SHA 及检查结果以 PR 正文为准。返工 Comment 草稿保留在 build/gate0/rework-comment.md，本次不另行发布；未授权合并。

本轮提交信息：`fix: 收紧导入确认与系统字段输入契约`。发布本轮修改后，仍需 A/B/C 交叉复核与非作者 R 正式结论；合并另行授权，合并 #2 不等于全体 Gate 0 通过。
