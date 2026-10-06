# C 轨 D2 双构建配置（完成记录）

- 交接依据：[开发规划](../../退休人员名册打印小程序开发规划.docx) 第 5 节 D2-C 卡、[七阶段开发任务清单](../../../reference/七阶段开发任务清单.xlsx) 第 A15 行
- 完成日期：2026-10-05；返工更新：2026-10-06（按 PR #10 Formal Review）
- 状态：**COMPLETE（候选）** —— 双构建配置与空程序候选包已建立；正式 Gate 1 结论由非作者 R 给出
- 基线依据：[OD-0002](../../decisions/OD-0002-Windows7-SP1目标基线.md)（Windows 7 SP1 / 6.1.7601 / x86/x64）
- 工具集与镜像口径依据：[OD-0003](../../decisions/OD-0003-D2正式构建工具集与镜像口径.md)

## 一、完成定义对照

| 完成定义 | 状态 | 证据 |
| --- | --- | --- |
| `CMakeLists.txt`（正式构建与发布入口） | 完成 | 仓库根 `CMakeLists.txt`；[配置对照](config-comparison.md) |
| `xmake.lua`（辅助镜像） | 完成 | 仓库根 `xmake.lua`；[配置对照](config-comparison.md) |
| 两套可复现命令 | 完成 | [cmake-configure.txt](cmake-configure.txt)、[xmake-configure.txt](xmake-configure.txt) |
| 工具集选择受控（`-T v141_xp` + 断言） | 完成 | [cmake-toolset-assertion.txt](cmake-toolset-assertion.txt)、[OD-0003](../../decisions/OD-0003-D2正式构建工具集与镜像口径.md) |
| 配置对照 | 完成 | [config-comparison.md](config-comparison.md) |
| 依赖检查结果 | 完成 | [dumpbin-cmake-app.txt](dumpbin-cmake-app.txt)、[dumpbin-xmake-app.txt](dumpbin-xmake-app.txt) |
| CMake 候选空程序 | 完成 | [cmake-install.txt](cmake-install.txt)、`dist/candidate/app.exe` |
| Win7 SP1 x86/x64 启动证据 | 完成 | [x86-CMake候选空窗口.png](x86-CMake候选空窗口.png)、[x64-CMake候选空窗口.png](x64-CMake候选空窗口.png) |

## 二、工具链（toolchain-versions.txt）

- Visual Studio 2017 Build Tools 15.9：MSVC 14.16.27023（cl 19.16.27054），平台工具集 `v141_xp`（Win32 与 x64），Windows 7.1A SDK。
- CMake 3.15.7（正式入口）；XMake 2.9.9（辅助镜像）；dumpbin 14.16.27054.0。
- 正式工具集只由命令行 `-T v141_xp` 选择；`CMakeLists.txt` 不修改 `CMAKE_GENERATOR_TOOLSET`，仅在 `project()` 后断言实际工具集（OD-0003）。

## 三、构建与测试结果

| 流水线 | 结果 | 证据 |
| --- | --- | --- |
| CMake 配置（受控命令 `-T v141_xp`） | 成功，`PlatformToolset=v141_xp` | [cmake-configure.txt](cmake-configure.txt) |
| 工具集断言 | 未带 `-T v141_xp` 的配置被拒绝并报错 | [cmake-toolset-assertion.txt](cmake-toolset-assertion.txt) |
| CMake 构建（全新 build 目录） | 成功；`app.exe`、`roster_sqlite.lib`、9 个测试 exe | [cmake-build.txt](cmake-build.txt) |
| CTest | 9/9 通过 | [ctest.txt](ctest.txt) |
| XMake 配置 | VS2017 / MSVC 19.16.27054 | [xmake-configure.txt](xmake-configure.txt) |
| XMake 构建（clean） | 成功 | [xmake-build.txt](xmake-build.txt) |
| XMake 测试 | `roster_tests` 全部通过 | [xmake-tests.txt](xmake-tests.txt) |

测试集：`build_config_test`（锁定宏与 `/MT` 自检）、`sqlite_smoke_test`（SQLite 3.45.3 静态链接自检）、既有 7 个契约消费者。

## 四、产物与依赖检查

- `app.exe` 73,216 字节；依赖仅 `USER32.dll`、`KERNEL32.dll`，无 MSVCR/UCRT → `/MT` 静态运行库确认（[dumpbin-cmake-app.txt](dumpbin-cmake-app.txt)、[dumpbin-xmake-app.txt](dumpbin-xmake-app.txt)）。
- PE 头：machine x86 (14C)，linker 14.16，subsystem 5.01（Windows GUI）（[dumpbin-cmake-app-headers.txt](dumpbin-cmake-app-headers.txt)）。
- 候选包布局：`app.exe` + `data/`、`templates/`、`backups/`、`exports/`、`logs/`、`docs/`（[cmake-install.txt](cmake-install.txt)）。

## 五、Win7 SP1 启动证据

- 主机虚拟机：`Win7RTM-SP1-x86`（6.1.7601，x86）、`Win7RTM-SP1-x64`（6.1.7601，x64），均来自 D1 `00_Base` 基线。
- 传输方式：只读 ISO（`roster-d2c.iso`，卷标 `ROSTER_D2C`）经 SATA 光驱送入 Guest，不安装 Guest Additions、不污染基线。
- 结果：32 位 CMake 候选包在两台 VM 均启动空窗口，标题正确显示“退休人员名册打印小程序”；x64 经由 WOW64 运行。截图采集于返工后重建的候选包。
- 运行后已恢复：x86 保存状态；x64 关机；光驱与端口数恢复原值。

## 六、第三方依赖

- 5 个固定源包已归档于本地 `third_party/archives/`（不入库），SHA-256 记录见 [third_party/README.md](../../../third_party/README.md)。
- SQLite 3.45.3 amalgamation 已 vendored 到 `third_party/sqlite/` 并纳入两套构建（`roster_sqlite`）；[依赖台账](../../dependencies/THIRD_PARTY.md)已同步。
- xlsxio_read / Expat / zlib / libxlsxwriter 在各自被消费的任务卡（D3 导入、D5 导出）纳入，纳入前不链接。

## 七、改动文件

```text
CMakeLists.txt                       正式构建与发布入口（-T v141_xp + 断言）
xmake.lua                            辅助开发镜像
src/ui/main_win32.cpp                空窗口候选程序（B 轨 D2-B 将扩展为界面骨架）
tests/build_config_test.cpp          构建配置自检
tests/sqlite_smoke_test.cpp          SQLite 静态链接自检
third_party/README.md                依赖归档与 SHA-256
third_party/sqlite/                  SQLite 3.45.3 amalgamation
packaging/package/                   候选包目录骨架
docs/decisions/OD-0003-*.md          工具集选择与镜像口径决定
docs/dependencies/THIRD_PARTY.md     依赖台账同步
.gitignore                           排除第三方源包归档
```

## 八、已知边界与待办

- xlsxio_read/Expat/zlib/libxlsxwriter 未接入：属于 D3/D5 消费依赖，不在本卡范围。
- XMake 使用 v141 编译器但不启用 `v141_xp` 平台工具集：按 [OD-0003](../../decisions/OD-0003-D2正式构建工具集与镜像口径.md) 作为受控口径，正式候选包只由 CMake 生成。
- `v141_xp` 构建产生 MSB8051 弃用提示（VS 通用提示），不影响构建与运行；日志中该本地化提示已归一化。
- 本卡只证明“空程序启动”；导入、维护、筛选、导出与 L2/L3 完整链路属于后续卡与 Gate。
- Gate 0 正式签认前继续 D2-C 已由 OD-0003 记录为受控预开发例外；Gate 1 结论仍由非作者 R 给出。
