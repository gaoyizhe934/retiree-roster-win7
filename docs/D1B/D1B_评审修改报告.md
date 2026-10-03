# D1B CV4 使用流程与模板设计评审修改报告

阶段D1B，设计日期2026-10-01；最后修订2026-10-03。ContractVersion 4 Draft，Gate 0 未通过，非作者 R 未代签。唯一阶段成果PR为#3，平台状态/当前head/Review以GitHub为准。

## 既有CV4主体

既有27/28显式映射、FieldChange payload/clear、可信preview与immutable checked copy、Confirm源身份核对、total_count()派生、YearCount shape、筛选白名单/类型比较、Unknown日期、既有状态日期单入口和报告默认禁用保持。原先旧#1/双父历史污染已在上一轮清理，本轮不再重建PR或改写历史。

## 2026-10-03 SP1 基线同步

PR #8 已 APPROVED 并合并，OD-0002 Accepted；SP1固定内容锚点 `a0dfdd8e373ae90f765c20cf8c075a8754f674bd`。当前性目标改为 Windows 7 SP1 / 6.1.7601 x86/x64；需求/规划 v2.1、SP1任务台账三份指纹同步；业务样表指纹和公共契约完全不变。OD-0002只覆盖OS，DTO/API、ContractVersion、Win32/x86主发行架构保持。

Q1-B/Q2-A已经取得：首期只有当前业务工作簿，P1行1/52标题与P2行3/23标题均为首期Source Profile；ImportProfile仍未冻结。Q01/Q02/Q05移除已回答的范围问题，保留HEADER-ONLY/0行、日期/枚举/真实批次状态、数据级脱敏测试样本、5 Unsupported与8语义项的责任边界，不采用未合并#6详细草案为权威。P11/P12既有控件增加只读说明，不重构CV4主体。

生成器以固定内容锚点定位资料链接及指纹；current main、阶段head、merge-base、ahead/behind和Draft/Ready移至PR/发布快照/Formal Review。新增SP1/7601/v2.1/OD/handoff/Owner决定防回退及故意损坏反例，六份MD/HTML/JSON产物重新生成，真实数量见证据JSON。

本轮HTML仅增量目视：环境、Q项、来源链接和长表溢出；CSS与HTML LF规则保持，完整视觉QA历史保留。当前非Git固定基线验证副本检查不等于阶段分支已纳入SP1；整合经GitHub integration PR、明确合并授权和必要评审，阶段成果仍由#3承载。

整合/发布后需在实际head重验；最终push且behind=0后再切Ready并请求非作者R Formal Review。作者检查、Owner决定与PR2/PR8合并均不代表Gate 0 PASS；Win32/导入事务/GDI/xlsx/实物打印/Win7 SP1 VM未由本轮验证。
