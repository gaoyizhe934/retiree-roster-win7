# C 轨 D1 环境与 VM 基线冻结（完成记录）

- 交接依据：docs/status/C轨D1交接说明_2026-10-02.md（原 DSH 主机历史交接记录，含原工具链信息）、docs/status/C轨D1接手核查记录_2026-10-02.md（本机接手记录）
- 完成日期：2026-10-03
- 状态：**COMPLETE（候选）** —— VM 基线已建立；正式 Gate 0 结论由非作者 R 给出
- 基线调整记录：项目基线已由用户确定为 **Windows 7 SP1（6.1.7601）**（发行量最大、介质可靠、贴近单位实际环境），替代原需求中的 Windows 7 RTM 6.1.7600（非 SP1）。**SP1 7601 为当前有效基线**，本记录及其证据均以该版本为准。

## 一、介质台账

| 架构 | 文件名 | 大小（字节） | SHA-1 | 校验结果 |
| --- | --- | --- | --- | --- |
| x86 | cn_windows_7_ultimate_with_sp1_x86_dvd_u_677486.iso | 2,653,276,160 | B92119F5B732ECE1C0850EDA30134536E18CCCE7 | **通过**（与官方 MSDN 校验值一致） |
| x64 | cn_windows_7_ultimate_with_sp1_x64_dvd_u_677408.iso | 3,420,557,312 | 2CE0B2DB34D76ED3F697CE148CB7594432405E23 | **通过**（与官方 MSDN 校验值一致） |

- 来源：MSDN 官方原版镜像（文件名、大小、SHA-1 与 rg-adguard 官方库一致）
- 安装后系统：Windows 7 旗舰版，版本 6.1.7601（SP1），x86 / x64

## 二、VirtualBox VM 配置与 00_Base

| 项 | Win7RTM-SP1-x86 | Win7RTM-SP1-x64 |
| --- | --- | --- |
| OS Type | Windows 7 (32-bit) | Windows 7 (64-bit) |
| 内存 | 2048 MB | 4096 MB |
| CPU | 2 | 4 |
| VRAM | 128 MB | 128 MB |
| 硬盘 | 40 GB VDI（D:\VMs） | 40 GB VDI（D:\VMs） |
| 网络 | NAT | NAT |
| 光驱 ISO | cn_windows_7_ultimate_with_sp1_x86_dvd_u_677486.iso | cn_windows_7_ultimate_with_sp1_x64_dvd_u_677408.iso |
| 00_Base 快照 | **已建立**（UUID abddf116-23e8-4925-b26b-7479239d8592） | **已建立**（UUID 79afe513-67c4-4227-9d3c-7429db180adc） |

快照描述：`Windows 7 Ultimate SP1 (6.1.7601) x86/x64 纯净基线：无Office、无VC++ Redistributable、无额外.NET`

## 三、系统纯净性确认

- 版本：Windows 7 旗舰版，6.1.7601（SP1）
- 无 Microsoft Office
- 无主动安装的 VC++ Redistributable
- 无额外 .NET Framework 4.x（系统自带 .NET 3.5.1 保持默认）
- 未安装 VirtualBox Guest Additions（符合交接文档"Gate 0 不依赖 Guest Additions"）

### Guest 内证据（截图，2026-10-03 采集）

每个 VM 三组截图，保存在本目录：

| 证据 | x86 | x64 |
| --- | --- | --- |
| 系统版本（winver：Windows 7 旗舰版 / 6.1.7601 SP1） | `x86-winver-关于Windows.png` | `x64-winver-关于Windows.png` |
| 已安装程序列表（程序和功能，无 Office/VC++/额外.NET） | `x86-programs-程序和功能.png` | `x64-programs-程序和功能.png` |
| systeminfo（OS 版本/系统类型，文本过长分两张） | `x86-systeminfo-part1.png`、`x86-systeminfo-part2.png` | `x64-systeminfo-part1.png`、`x64-systeminfo-part2.png` |

截图由维护员按 C 轨 D1 步骤在 Guest 内采集并经人工核对无异常。

## 四、BLOCKER-01 状态变更

**BLOCKER-01：RESOLVED**（保留历史）

原描述：缺少可信合法来源的 Windows 7 RTM 6.1.7600 x86/x64（非 SP1 / 非 7601）安装介质。

解决路径：
1. 与用户协商，基线由 RTM 7600 调整为 SP1 7601（发行量最大、介质可靠、贴近单位实际环境）。
2. 获取官方原版 SP1 镜像并完成 SHA-1 校验（两份均通过）。
3. 创建 x86/x64 两台 VirtualBox VM 并完成纯净安装。
4. 两台 VM 均建立 `00_Base` 快照。

## 五、文件传输路径（建议，沿用交接文档）

- Host 样表目录：`D:\retiree-roster\testdata\sanitized\`
- Guest 目录：`C:\roster-test\samples\`、`C:\roster-test\candidate\`、`C:\roster-test\work\`、`C:\roster-test\out\`
- 传输方式：Host → ISO/只读虚拟介质 → Guest（不装 Guest Additions、不污染纯净基线）

## 六、仍待 C 轨完成项（不阻塞 VM 基线）

- C-G0-01：VS2017 15.9 / v141_xp / Win32 x86 / C++14 / /MT 编译运行 6 个契约消费者——**本机无 VS2017 工具链**，需在具备该工具链的主机执行。
- C-G0-02：D2 正式工程建立后，CMake 与 XMake 编译一致性核对。
- C 轨原始 10 个证据文件（原 DSH 主机）是否入库，由 C 轨与 R 决定。

## 七、交接结论

C 轨 D1 的 VM 基线部分已完成（双 VM + 00_Base + 介质校验 + Guest 内证据）。正式 Gate 0 结论由非作者 R 结合 A/B/C 交付统一判断；当前有效基线为 Windows 7 SP1（6.1.7601）。