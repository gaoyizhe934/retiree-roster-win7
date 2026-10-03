# OD-0002 Windows 7 SP1 目标基线

状态：Accepted，仅限目标操作系统条款。决定来源：仓库创建者在本任务的直接请求；记录及生效日期：2026-10-03。仓库内修订文件作为新 PR 候选，进入 main 仍须非作者评审和独立合并授权。

## 请求与适用范围

创建者提供《D1A_Q1_Q2与Windows7_SP1详细修改清单.md》，并直接要求：

> 阅读，创建新的分支和pr，按照清单内容决定进行仓库统一

本次据此实施清单第十至十七节的 SP1 基线统一。附件中“用户现已明确要求”的陈述不是独立审批证据；本记录依据以上当前请求，不补造早先批准或另行甲方签字。

| 条款 | 当前决定 |
| --- | --- |
| 目标 OS | Windows 7 SP1，版本 6.1.7601 / build 7601 |
| 架构 | x86 与 x64，两台 VirtualBox 纯净来宾 |
| 主发行包 | Win32 / x86，32 位原生 exe |
| API level | WINVER=0x0601、_WIN32_WINNT=0x0601 |
| 纯净条件 | SP1 已安装；不额外安装 Office、.NET 或 VC++ Redistributable |
| 覆盖旧条款 | v2.0 中 Windows 7 RTM / 6.1.7600 / 不安装 SP1 的当前目标环境要求 |
| Edition | 不新增限制；当前 C VM 的简体中文旗舰版只是实际实例 |

SP1 不改变 Windows 7 API level、C++14、静态依赖、VS2017/v141_xp、主发行架构或业务 DTO/API。ContractVersion 保持 4 Draft，DatabaseSchemaVersion 仍独立未分配。

## 权威文件与历史

仓库内[需求说明 v2.1](../退休人员名册打印小程序需求说明.docx)和[开发规划 v2.1](../退休人员名册打印小程序开发规划.docx)增加修订记录；[任务台账](../../reference/七阶段开发任务清单.xlsx)仅修改九个 OS 环境单元格，表结构、进度与 R 结论保留。旧 v2.0 和旧指纹可从 main 起点 `567d9cd32befc2b8aa7ae99487f8b6d2170f1436` 复核。目录外原始资料和业务工作簿不修改。修订后指纹见[基线来源](../baseline/00_基线与权威来源.md)。

历史 Review 中 RTM 是当时要求，保留原文；当前要求由本决定替代。VM 名称及 VBoxManage、ISO、Guest 的原始输出不得手工改写。历史 VM 名称包含 RTM 时应在说明中解释，若重命名则重新采证。

## 验证与后续

本决定解决目标环境的 RTM/SP1 条款冲突，不证明 VM 内的系统版本、软件清单、L2/L3、字体/DPI/设备、GDI/xlsx 或实物打印已经通过。C 的 Guest 证据和交接来源/链接问题仍独立闭环。

新基线合入 main 后，#3/#6/#7 继续各自唯一阶段 PR，按[跨轨交接](../status/SP1_BASELINE_HANDOFF.md)纳入基线并复跑。所有分支整合经 GitHub PR，不使用本地 merge、rebase 或会生成合并提交的 pull。此决定及 PR Approval 均不构成 Gate 0 PASS。
