# Gate 0 稳定化交接与修改报告

日期：2026-10-01。任务：依据《仓库矛盾修复与稳定化修改清单》完成 S1 本地稳定化候选，不进入 D2 功能开发。

起点：origin/main `af0ae01981ac3d65653921ceada1cee605de5607`。分支：`fix/gate0-baseline-stabilization`。本记录保存提交前审核结果；创建者已明确授权本轮 commit、push 和创建修复 PR，合并仍未授权。D1B 在其原分支保留，未混入本分支。

## 六项工作与进度

| 工作 | 验收 | 状态 |
| --- | --- | --- |
| 1 仓库与基线 | 保留原工作，核对 main 及四份原始文件指纹 | 完成 |
| 2 P0 契约草案 | 23 列、日期、标签、编号、筛选、快照、模板、批次／日志 | 完成，待共同复核 |
| 3 基线与仓库规则 | 入口、权威顺序、ADR、忽略、命名与 PR 规范 | 完成 |
| 4 可复现验证 | 仓库内检查脚本、日期行为、消费者、验收数据 | 完成，9/9 检查通过 |
| 5 双轴审查 | Standards／Spec 的独立作者辅助审查及修复 | 完成，两项 P2 已修复并定向复核 |
| 6 交接 | 逐文件原因、真实测试结果、未完成项与下一起点 | 完成 |

本轮本地候选进度 6/6（100%），不代表整份清单或 Gate 0 已完成。

## 逐文件修改原因

| 文件 | 原因 |
| --- | --- |
| include/retiree_roster/schema_types.hpp | Draft revision 2；补 Person 字段与精度、移除双重关怀真值、补筛选及快照输出／版式／审计对象 |
| README.md | 改为入口，移除第三行永久模板与 Schema 自封基线 |
| CONTRIBUTING.md | ASCII 分支、按任务卡划分 PR、非作者签认与 Gate 入口 |
| GitHub协作命名规范.md | 补齐原缺失链接，明确最新命名与逐项发布授权 |
| .gitignore | 隔离构建产物、本地数据库／备份／导出／日志和中间文件 |
| .gitattributes | 文本 LF、脚本平台换行、Word／Excel 二进制 |
| .github/pull_request_template.md | 任务、修改、证据、隐私、未决项和 R 结论固定格式 |
| docs/baseline/00_基线与权威来源.md | 七层来源、批准边界、原文件指纹及遗留本地资料冲突提示 |
| docs/baseline/01_导入Profile冻结说明.md | 未冻结 Profile、预填／预检／确认、缺失状态与重复阻断 |
| docs/baseline/02_字段映射与数据保留策略.md | 23 列逐一映射，保留／阻断三种处置及隐私策略 |
| docs/baseline/03_标识符与编号口径.md | 内部 ID、源工号、固定业务编号、当次序号分离 |
| docs/baseline/04_本地操作员说明.md | UserId 等字段为本地归属，非身份认证 |
| docs/baseline/05_筛选与打印契约.md | R01–R05、逻辑组合、模板尺寸与后续接口验收 |
| docs/decisions/ADR-0001-仓库基线权威顺序.md | 记录基线覆盖原则的待审提案 |
| docs/decisions/ADR-0002-日期精度模型.md | 记录不伪造日期及可计算精度的待审提案 |
| docs/decisions/ADR-0003-名单快照与输出一致性.md | 记录同快照输出及数据变更失效的待审提案 |
| docs/decisions/ADR-0004-标签与关怀状态模型.md | 记录标签唯一来源与年度慰问的待审提案 |
| docs/dependencies/THIRD_PARTY.md | 固定五类依赖、上游许可证与传递组件待核项 |
| docs/status/GATE_STATUS.md | 初始化单一 Gate 台账，不填写通过结论 |
| docs/status/STABILIZATION_REVIEW.md | 本轮范围、逐文件说明、验证与交接 |
| tests/contract/date_value_test.cpp | 通过公共接口验证精度、日期合法性、世纪闰年与禁止伪造日 |
| tests/contract/consumer_contract_test.cpp | C++14 消费者、字段元数据和只读输出视图检查 |
| tests/contract/chongyang_cases.csv | 13 个脱敏 R02 预期案例，含 89/90/91 和去世 90 |
| tools/gate0/check_contract.py | 离线可复现检查与命令／指纹证据，失败非零 |
| tools/gate0/README.md | 一条运行命令、检查范围和验证边界 |

Diff 摘要：修改三份原文件、新增 22 份治理与验证文件，共 25 份候选文件；没有修改原始 Word／Excel、D1B 内容、数据库实现、Win32、GDI 或 xlsx 功能。

开工前已有的未跟踪 CONTEXT.md、docs/adr/ 和目录说明保留原文，不纳入本轮候选。其旧术语与本轮草案有冲突，已在基线说明标明，不把其内容视为批准决定。

## 验证结果

命令：`python tools/gate0/check_contract.py`；整改后 9/9 检查通过，退出码 0。输出只保存在被忽略的 build/gate0/results.json，含全部被检查源文件指纹、工具版本、命令、退出码及负例诊断。日期测试在旧契约上因缺少 DateValue 编译失败，修改后编译和执行均通过。

| 检查 | 实际结果 |
| --- | --- |
| 原始资料指纹 | 四份基线保持原值 |
| 第 3 行源字段 | 23/23 映射到字段元数据与 Person 成员，W 空列／X 备注位置正确 |
| DateValue 行为 | 四种精度、闰年／世纪年、缺失／伪造日值；g++ C++14 编译／执行均退出 0 |
| 公共消费者 | 字段唯一性、Unknown／Unspecified 初始状态、模板与只读快照视图；编译／执行均退出 0 |
| 旧接口拒绝 | 正常 syntax 对照成功；4 个旧／可变接口消费者被编译器明确拒绝 |
| R02 预期数据 | 13 条包含 89/90/91 与去世 90；只核对验收数据完整性，未执行规则引擎 |
| 忽略／属性 | 12 个私有产物探针被忽略，6 个必要资源探针保留，Word／Excel 为 binary |
| 文档链接 | 17 个本轮 Markdown 中 34 个本地链接有效 |
| Diff | 提交前 git diff --check 通过；审核时暂存区为空 |

编译器为开发机 MinGW GCC 6.3.0，以 -std=c++14 -Wall -Wextra -pedantic-errors 检查；未将其当作正式发布工具链。

## Standards

独立辅助审查发现 1 项 P2：负例检查可能把工具失败计为 PASS，证据输入／版本记录不完整。已加入同模式正常对照、严格编译错误分类、各负例诊断与命令、完整输入指纹及工具版本；定向复核确认源码修复闭环，最终运行刷新证据。剩余发现 0。

## Spec

独立辅助审查发现 1 项 P2：Party50 草案额外限定在世，超出 R03。已改为服从显式状态，FilterSpec 初始为 Unspecified，Party50 UI 默认待业务确认；定向复核无剩余发现。辅助审查不构成 R／A/B/C 正式签认。

未运行：正式 MSVC2017 v141_xp／CMake／XMake、SQLite 事务、业务规则引擎、快照失效集成测试、GDI、xlsx、Win7 L2/L3 与物理打印。当前没有产品实现或正式工程骨架，不能把结构检查写成这些功能通过。

## 清单范围与未完成项

- P0-01–P0-11：本轮落地候选文件／契约，均待 A/B/C/R 及适用业务确认；不是 Gate 冻结。
- P0-12、P1-03–P1-05：依清单 S4，稳定化合入后再返工 #1 的字段表、Q 项、MD／HTML、历史记录和可复现证据；本轮保留 #1。
- P1-01/02/06/07/08/09/11：入口、任务卡 PR、忽略、属性、模板、台账、本地操作员说明已准备。
- P1-10：13 个边界预期数据已准备；D4 规则引擎测试尚未执行。
- P1-12：依赖台账已建立，固定源码包、传递组件、notice 与 Win7 验证尚未闭环；项目 LICENSE 待创建者选择。
- P2-01/02：删除远程旧分支、修改保护规则不属于本轮已执行操作，仍待创建者审查；P2-03 已通过入口化 README 处理。2026-10-01 只读核实 [#1](https://github.com/gaoyizhe934/retiree-roster-win7/pull/1) 为 Open／Draft，main 和两条已有 docs 分支均 protected=true，旧贡献指南分支仍与 main 同 SHA；未改变任何远程状态。

甲方待确认：固定编号格式以及工号等价关系、无状态列时的业务选择、模板具体参数、第二份样表。A/R 待确认：重复候选规则、枚举／党员代码与 Profile 唯一匹配。C 待补：环境与固定依赖实际构建。R 待给出正式非作者结论。

## 下一步与发布候选

本轮已通过创建者提交前审核并获 commit、push、创建修复 PR 的明确授权。提交信息：`fix: 统一Gate0基线与公共契约`。PR 用于 A/B/C/R 共同复核 Proposed ADR、契约及剩余业务确认；发布不代表契约批准或 Gate 通过，合并仍须单独授权。

稳定化获准合入后，按清单 S4 同步并返工 #1，再由 R 重新审查。B 轨合并不等于全体 Gate 0 通过，不能据此进入 D2。
