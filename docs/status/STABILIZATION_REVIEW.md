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

## 2026-10-02 R Review 返工

以上章节保留 2026-10-01 审核历史；以下为本轮新记录。来源为[最新 R Conversation 意见](https://github.com/gaoyizhe934/retiree-roster-win7/pull/2#issuecomment-5943240204)与创建者提供的《PR2_最新Review后详细返工清单》。已核对本地／远端 HEAD 同为 279a204aaf00233fac262f79ac4e3dd80d392f21，base／merge-base 为 af0ae01981ac3d65653921ceada1cee605de5607；主分支未变，不执行本地分支合并。

R 的原意见未发现 Bug／Blocker，独立结构层 7/7 通过，C++ 层未独立复跑。本轮不覆盖该历史结论，也不把作者候选当作 R 新签认。ContractVersion 从 Draft 3 递增到 4，仅表示破坏性契约修订。

### Risk 处理

| Risk／清单 | 本轮修改 | 责任与当前状态 |
| --- | --- | --- |
| R01／F-01 | ImportFieldId／EditableFieldId 独立值域，try_to_person_field 的 switch 按名称映射；转换失败不写 out，空指针拒绝；业务验证不再 cast 成 FieldId | 契约候选已加固；27／28 合法目标和所有字节值检查通过，反序 PersonFieldId 的同一消费者通过，待 R 复核 |
| R04／F-02 | FieldChange 校验字段能力、日期／Text／EnumCode 载体与 clear 互斥；规范 Unknown 必须零组件，Identifier／Timestamp 拒绝 | 六个日期字段及非法载体回归通过；必填／值域／跨字段约束留 D3 |
| R05／F-03 | is_valid_year_count_condition：关闭不解释 payload，启用必须有集合或下限且无负值 | 结构用例通过；完整 FilterSpec 校验与实际年龄筛选留 D4 |
| R03／F-04 | 移除可写 total_count，total_count() const 返回 rows.size() | 空名单、37／36 人及只读消费通过；旧字段写入编译负例纳入 runner |
| R02／F-05 | ImportPreviewRequest 标注不可信提案；Profile 文档补 15 项强制表及 D3 集成用例，明确源文件变化拒绝确认 | #2 完成边界说明；服务校验、不可变缓存、摘要一致性、事务与幂等仍待 D3，风险未冒充实现闭环 |
| F-06 | 记录现有 Conversation 与 Formal Review 区别，准备新 HEAD 复核请求 | 平台 reviews 当日核对为 0；新候选尚未提交发布，正式 R Review 暂不能指向新 HEAD |

Import/Edit 的底层数值只属于各自输入类型，不能作为 PersonFieldId／数据库／模板编号持久化。合法强转可能只表达白名单中的业务字段，无论数值来自何处，都不能转出系统字段；未知值拒绝。原系统字段保护回归保留，新增全值域枚举检查避免未来 canonical 重排改变测试含义。

### 本轮逐文件原因

| 文件 | 修改原因 |
| --- | --- |
| include/retiree_roster/schema_types.hpp | 显式映射、payload／年份结构验证、单一计数、提案边界、Draft 4 |
| tests/contract/enum_field_mapping_test.cpp | 全部命名目标、无效值、空 out、白名单回归 |
| tests/contract/field_change_test.cpp | 六类日期字段与文本／枚举／clear 值载体约束 |
| tests/contract/filter_shape_test.cpp | 空启用、集合、下限、负值与关闭语义 |
| tests/contract/input_authority_test.cpp | 原权限保护加全部底层值映射白名单检查 |
| tests/contract/consumer_contract_test.cpp | 年份条件消费者与人数单一来源 |
| tools/gate0/check_contract.py | 三项新检查、反序 canonical 变体、计数／编辑系统字段负例、每层身份与命令诊断 |
| tools/gate0/README.md | 新检查范围、反序产物及分层证据保留说明 |
| docs/baseline/01_导入Profile冻结说明.md | 不可信提案、15 项 D3 行为与集成验收 |
| docs/baseline/05_筛选与打印契约.md | Draft 4、年份／字段结构边界、派生人数 |
| docs/decisions/ADR-0003-名单快照与输出一致性.md | 移除独立可写人数并保留 Proposed |
| docs/status/GATE_STATUS.md | Gate 与 PR 候选结论分离，修正 D1B 最新 #3 引用 |
| docs/status/GATE0_REVIEW_HANDOFF.md | C 正式工具链和 R Formal Review 可领取交接，保留 A／B 缺口 |
| docs/status/STABILIZATION_REVIEW.md | 追加本轮来源、风险、逐文件与验证证据，保留旧历史 |

### 本轮验证与交接

Red 已复现：旧契约没有显式映射／年份校验接口，日期字段接受混合文本，RosterResult 的可写字段不能满足只读派生计数调用。修复后逐层验证如下，不继承旧 12/12 数字；定稿后刷新同一候选的最终证据。

| 命令（均以 python tools/gate0/check_contract.py 开始） | 结果 | 证据 |
| --- | --- | --- |
| --layer structure --base-ref origin/main | 7/7，退出 0，编译器未执行 | build/gate0/oct02-structure-results.json |
| --layer cpp14 --base-ref origin/main | 8/8，退出 0 | build/gate0/oct02-cpp14-results.json |
| --layer diff --base-ref origin/main | 1/1，退出 0 | build/gate0/oct02-diff-results.json |
| --layer all --base-ref origin/main | 15/15，退出 0 | build/gate0/oct02-all-results.json |

Python 3.12.14；MinGW GCC 6.3.0，-std=c++14 -Wall -Wextra -pedantic-errors。27 个旧接口／越权消费者被编译拒绝，正常语法控制通过；27／28 个显式目标在普通及 canonical 反序声明下均正确。六个日期字段、文本／枚举／clear、年份结构及名单计数消费者通过。4 份原始资料指纹、23 列映射、13 条 R02 预期数据、12 个忽略与 6 个公开资源探针均通过；19 份 Markdown 的 43 个本地链接有效。R02 数据未执行年龄规则。

每个执行层记录 base／merge-base／当前 HEAD、Python／编译器、原样命令（含 Git 进程内 safe.directory 例外）、退出码／诊断及 37 份输入指纹。编译器版本、每次 compile／run 与 27 条拒绝诊断均在 JSON 中。PR 已提交 Diff、暂存和工作区空白检查退出 0，暂存区为空。

所有证据只标识已提交 HEAD 279a204 及当前输入指纹；本轮尚无新 HEAD，不填未来 SHA。发布后必须在同一新提交上重跑并更新 PR 证据。分层 JSON 集中保存在被忽略的 build/gate0。

正式 MSVC2017/v141_xp／CMake／XMake、SQLite／revision 服务、规则引擎、快照失效、GDI／xlsx、双 Win7 RTM 与物理打印未运行。本机 cl／cmake／xmake 未在 PATH 发现，vswhere 查询 [15.0,16.0) 返回空列表，不将补充 g++ 结果替代正式 C 验收。C-G0-01／02／03 和 R 新 HEAD Formal Review 详见[复核交接](GATE0_REVIEW_HANDOFF.md)，当前是材料就绪待领取，未发送他人消息、未获得 C／R 接收或通过结论。

### Standards（本轮）

独立只读辅助审查发现 0 项。显式转换、结构约束、runner 证据与集中契约／C++14／原始资料保护符合记录标准；不代替正式 R。最终证据定稿只补实际数字和命令记录，未新增业务行为。

### Spec（本轮）

独立只读辅助审查发现 0 项。F-01～F-04 契约加固、F-05 D3 强制清单符合本轮要求，F-06 与 C 正式工作如实待交接／新 HEAD 复核。Gate 0 仍未通过；不代替正式平台 Review。

本轮继续原 #2，D1B 当前唯一有效 PR 为 #3，旧 #1 已关闭；此新引用替代上文历史中的 #1 后续描述。原有未跟踪资料保留。当前请求只授权修改，未执行 git add／commit／push、发布评论、Formal Review 或合并。建议提交信息：`fix: 加固字段映射与筛选结构契约`。本轮本地五项工作完成 5/5：来源核对、契约与回归、文档与合作材料、分层验证、双轴辅助审查与交接。正式 C／R 验收及发布是后续事项，不把本地完成冒充清单的全体合作签认完成。

### 本轮提交与评论授权

2026-10-02，创建者查看上述审核材料后明确要求“commit,comment”。以上保留提交前审核快照；随后将已审核的 14 个文件提交，并在原 PR #2 追加中文报告，提交后的确切 SHA 与重新运行结果记录在该评论中。本次未授权 push 或合并，评论必须区分本地新提交和仍为 279a204 的远端 PR HEAD；不把未推送返工描述成已进入远端 Diff。正式 C／R 复核需待新提交可获取后执行。
