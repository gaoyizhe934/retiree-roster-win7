# PR #2 最新 R Review 返工复核交接

日期：2026-10-02。阶段 PR 仍为 #2；D1B 后续材料归入唯一有效 #3，旧 #1 已关闭。依据：[R Conversation 意见](https://github.com/gaoyizhe934/retiree-roster-win7/pull/2#issuecomment-5943240204)及创建者提供的详细返工清单。

当前远端／本地已提交 HEAD 为 279a204aaf00233fac262f79ac4e3dd80d392f21。本轮 ContractVersion 4 是该提交之上的未提交候选，不把该 SHA 写成返工后的新 HEAD。新 SHA 须在发布后更新并让 R 固定该提交复核；验证详情见[返工报告](STABILIZATION_REVIEW.md)。

## C 轨正式工具链请求

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

## R 轨新候选复核请求

最新已核对 GitHub formal reviews 数为 0；现有意见是 Conversation comment。本轮尚无新提交，因而尚无可指向的新 HEAD Formal Review。作者不切换角色自签，也不以内部 Standards／Spec 辅助审查替代正式 R。

R 在发布后固定新 HEAD，至少核对：

1. R01：全部 import／edit 显式按名称转换；反序 canonical 枚举仍通过；所有合法目标不包含系统字段。
2. R04：日期／文本／枚举载体及 clear 互斥，规范 Unknown、无效日期、越权字段拒绝。
3. R05：YearCountCondition 空启用、负集合／下限被拒绝，集合加下限合法；D4 业务筛选尚未实现。
4. R03：total_count() 只有 rows.size() 来源，旧可写字段负例失败。
5. R02：不可信请求与服务生成可信预检分离；[D3 强制表](../baseline/01_导入Profile冻结说明.md)仍是待实现验收。
6. 新测试进入 Gate0 runner，structure／cpp14／diff／all 证据与实际输入指纹对应。
7. 四份原始 Word／Excel 指纹保持不变，Diff 只含本轮返工，未引入真实人员数据。
8. C 正式编译、服务集成、快照与 Win7 未运行项不冒充通过。
9. 对该 HEAD 提交 GitHub Formal Review；按实际结果 APPROVE／REQUEST_CHANGES／COMMENT，记录平台 Review URL。

若 R 判断候选可合并，APPROVE 正文仍应明确“PR #2 候选通过 ≠ Gate 0 通过，Gate 0 等待 A/B/C/甲方及剩余基线条件”。Review 不是创建者的合并授权。

## A／B 与后续责任

A 仍需给出第二份样表／脱敏样本、重复候选识别与人工处置、性别／类别／级别和党员代码、Profile 唯一匹配、缺状态源业务选择、工号与固定编号关系的可审查基线。

B 的字段分类、旧 CareFlags／TagCodes、导入 revision 流程、系统字段只读、日期精度、模板来源、snapshot_id、旧 Q 项及 MD／HTML 证据返工继续归入 #3。#2 未经授权合并前不替 B 宣布依赖已就绪；不重建该阶段 PR，也不在本地合并分支。

Gate 0 仍未通过，见[Gate Status](GATE_STATUS.md)。R02 服务验收留 D3，完整 FilterSpec／快照与业务规则留 D4，GDI／xlsx 与输出对账留 D5；本轮只关闭可在公共契约层验证的风险。
