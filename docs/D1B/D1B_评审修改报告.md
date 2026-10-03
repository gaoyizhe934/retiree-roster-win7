# D1B CV4 使用流程与模板设计评审修改报告

阶段D1B，设计日期2026-10-01；工具链最后修订2026-10-04。ContractVersion 4 Draft，Gate 0 未通过，非作者 R 未代签。唯一阶段成果PR为#3，平台状态/当前head/Review以GitHub为准。

## 2026-10-04 Formal Review 返工

对 2026-10-03 的 CHANGES_REQUESTED / HOLD 处理 14 条 finding，按 8 个根因集中加固生成器、测试和证据链。CV4 Person/Tag DTO、Profile、筛选、模板参数和业务流程保持；不修改 A/C、SP1 或 Gate Status。本节描述本地实现与复核入口，最终评审结论由非作者 R 在发布后实际 head 上给出。

| Finding | 本地处理与复核入口 |
| --- | --- |
| Critical cp936 | configure_machine_output 在输出入口统一 UTF-8；test_machine_output_is_utf8_under_cp936 验证 build、clean check、含中文 drift、零写入 |
| Warning cp936 | 与 Critical 同根因；子进程复制全部环境再设置 cp936 / UTF-8 mode=0，不用 UTF-8 环境掩盖输出问题 |
| 双重装配 | assemble_data 是字段、控件、输入枚举、完整 Tab 的唯一装配入口；反例仅 mutation |
| 死代码 write | 删除文本 write 助手；产物只用 UTF-8 write_bytes，HTML LF 属性保留 |
| 文本锚点 | semantic_anchors 作为承重正文文本单一来源；正文 placeholder 与检查共用；Tag、FilterSpec、D20、人数和 Source Profile 的可结构验证部分直接查数据/契约 |
| UNC/盘符探测 | classify_href 先协议和绝对路径拒绝，再 resolve / relative_to(ROOT)，最后 exists；mock 回归断言危险链接没有 exists 调用 |
| SVG/Mermaid | SVG flow model 从原有完整图提取，业务边不变；检查实际 SVG 与 Mermaid 的节点及全部核心边/条件标签，改名和改边反例均拒绝 |
| fixture 输入清单 | ROOT_INPUT_FILES 同时驱动生产输入指纹、缺文件检查和 fixture 外部文件复制 |
| baseline 缺失 | 输入缺失返回 structured failed JSON；cp936 下 build / check 返回1、不出现 traceback、不改 fixture |
| initial_focus | 本页 control_ids / create_only_control_ids membership；无操作项与 P15 执行期容器为显式例外；不存在 ID 反例拒绝 |
| repo slug | REPOSITORY_SLUG 单一常量，inline 与资料固定链接共享；交付 JSON 记录 repository_slug |
| struct parser | 简单数据成员支持无初始化、等号、非空/空花括号；平衡 struct body，并排除成员函数体 |
| javascript/data disputed | 显式协议白名单，同时检查 Markdown 与实际 a[href]；最小 CSP 允许既有 inline CSS，没有 data 协议放行 |
| 环境指纹 | tracked 证据只声明 UTF-8 规范；版本、平台、调整前 stdout 编码、utf8_mode 和 cp936 运行结果写入仓库外运行记录 |

正常生成、只读检查、原有及新增反例、默认中文 Windows / cp936 回归、缺文件、危险链接、parser、焦点、流程一致性和 autocrlf 检出均按清单验证。数量与通过状态以本轮实际 JSON、测试输出及运行记录为准，不把历史检查数字当作当前结果。

本轮先集中完成本地修改，再交还人工审核；获授权后使用一个 closure commit、一次 push，在远端最终 head 复验后更新正文/闭环评论并安排 R Review。当前实现记录不表示已提交、已发布或已获 Formal APPROVE。

## 既有CV4主体

既有27/28显式映射、FieldChange payload/clear、可信preview与immutable checked copy、Confirm源身份核对、total_count()派生、YearCount shape、筛选白名单/类型比较、Unknown日期、既有状态日期单入口和报告默认禁用保持。原先旧#1/双父历史污染已在上一轮清理，本轮不再重建PR或改写历史。

## 2026-10-03 SP1 基线同步

PR #8 已 APPROVED 并合并，OD-0002 Accepted；SP1固定内容锚点 `a0dfdd8e373ae90f765c20cf8c075a8754f674bd`。当前性目标改为 Windows 7 SP1 / 6.1.7601 x86/x64；需求/规划 v2.1、SP1任务台账三份指纹同步；业务样表指纹和公共契约完全不变。OD-0002只覆盖OS，DTO/API、ContractVersion、Win32/x86主发行架构保持。

Q1-B/Q2-A已经取得：首期只有当前业务工作簿，P1行1/52标题与P2行3/23标题均为首期Source Profile；ImportProfile仍未冻结。Q01/Q02/Q05移除已回答的范围问题，保留HEADER-ONLY/0行、日期/枚举/真实批次状态、数据级脱敏测试样本、5 Unsupported与8语义项的责任边界，不采用未合并#6详细草案为权威。P11/P12既有控件增加只读说明，不重构CV4主体。

生成器以固定内容锚点定位资料链接及指纹；current main、阶段head、merge-base、ahead/behind和Draft/Ready移至PR/发布快照/Formal Review。新增SP1/7601/v2.1/OD/handoff/Owner决定防回退及故意损坏反例，六份MD/HTML/JSON产物重新生成，真实数量见证据JSON。

本轮HTML仅增量目视：环境、Q项、来源链接和长表溢出；CSS与HTML LF规则保持，完整视觉QA历史保留。当前非Git固定基线验证副本检查不等于阶段分支已纳入SP1；整合经GitHub integration PR、明确合并授权和必要评审，阶段成果仍由#3承载。

整合/发布后需在实际head重验；最终push且behind=0后再切Ready并请求非作者R Formal Review。作者检查、Owner决定与PR2/PR8合并均不代表Gate 0 PASS；Win32/导入事务/GDI/xlsx/实物打印/Win7 SP1 VM未由本轮验证。
