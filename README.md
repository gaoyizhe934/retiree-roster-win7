# 退休人员名册打印小程序

面向 Windows 7 RTM 的单机离线程序：导入退休人员 Excel、维护档案、生成名单、导出 xlsx、预览和本机打印。

当前处于 Gate 0 基线稳定化阶段，公共契约为 Draft，尚无可运行程序。进入 D2 前需要 A/B/C 交付及 R 非作者签认。

## 基线入口

- [基线与权威来源](docs/baseline/00_基线与权威来源.md)
- [需求说明 v2.0](docs/退休人员名册打印小程序需求说明.docx)
- [开发规划 v2.0](docs/退休人员名册打印小程序开发规划.docx)
- [七阶段任务台账](reference/七阶段开发任务清单.xlsx)
- [Gate 状态](docs/status/GATE_STATUS.md)
- [导入 Profile](docs/baseline/01_导入Profile冻结说明.md)、[字段与数据保留](docs/baseline/02_字段映射与数据保留策略.md)、[编号口径](docs/baseline/03_标识符与编号口径.md)

公共契约见 [schema_types.hpp](include/retiree_roster/schema_types.hpp)，其冻结状态见 Gate Status。业务口径以基线及已批准的局部变更为准。

## 技术与开发入口

C++14、Win32/Common Controls、GDI、SQLite、静态 xlsx 读写；32 位主发行包，目标机不安装额外运行库或 Excel。正式构建使用 CMake，XMake 作辅助，具体约束见开发规划。

正式工程构建由 D2 的 C 轨建立。目前仅支持[稳定化契约检查](tools/gate0/README.md)，该检查不生成产品发行包，也不证明 Win7 兼容性。

| 目录 | 内容 |
| --- | --- |
| include/retiree_roster | 公共类型草案 |
| docs/baseline、docs/decisions | 基线、源字段、导入与待审 ADR |
| docs/status、docs/dependencies | Gate、修复交接与许可证台账 |
| reference | 无个人数据的表头样表与任务台账 |
| tests/contract、tools/gate0 | 契约验证、规则验收数据与可复现检查 |

## 贡献与数据边界

见 [CONTRIBUTING.md](CONTRIBUTING.md) 和 [GitHub 协作命名规范](GitHub协作命名规范.md)。本地维护员标识只用于日志归属，见[操作员说明](docs/baseline/04_本地操作员说明.md)。第三方及项目许可证状态见[依赖台账](docs/dependencies/THIRD_PARTY.md)。

公开仓库仅存放无个人数据的模板、脱敏测试与源码。真实人员资料、数据库、备份、导出和日志在本地保管；忽略规则不能保护已跟踪文件，发布前仍须检查变更。
