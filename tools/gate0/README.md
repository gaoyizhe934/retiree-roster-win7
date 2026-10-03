# Gate 0 稳定化检查

在仓库根目录执行（Python 3 标准库，完整检查另需 PATH 中的 g++ 支持 C++14）：

```text
python tools/gate0/check_contract.py
```

没有 MinGW 的标准 Windows 开发机可先运行 Python 结构层，C++14 编译层与正式工具链层分别执行：

```text
python tools/gate0/check_contract.py --layer structure
python tools/gate0/check_contract.py --layer cpp14
python tools/gate0/check_contract.py --layer diff --base-ref origin/main
```

--layer structure 不执行 g++，--layer cpp14 不代替正式 MSVC2017 v141_xp／CMake 检查。默认 all 执行全部补充契约检查，缺少编译器时明确失败；分层结果保存 layer 和未执行层，不把部分检查写成全套通过。正式工具链及 Win7 验证仍由 C 轨在工程骨架齐备后执行。

脚本仅读取仓库内基线、样表表头、字段契约和本轮文档；输出到被忽略的 build/gate0。结果写入 results.json，含源码指纹、实际命令和退出状态，失败返回非零。没有网络请求或真实人员数据输入。

检查范围：受控基线指纹、23 列映射与头文件成员、日期结构行为、C++14 消费者编译／执行、revision 确认模型、系统字段能力与强转伪造拒绝、旧接口编译拒绝、重阳节边界验收数据完整性、忽略规则、二进制属性、文档链接与 Diff 空白。

cpp14 增加 enum_field_mapping（27 个导入／28 个编辑目标、未知值、反序 PersonFieldId 声明后的同一消费者）、field_change_value_kind（日期／文本／枚举与 clear 互斥）、filter_shape（YearCountCondition 的集合／下限与负值）。普通消费者验证 total_count() 从行集合派生，负例验证不可直接写人数。反序头文件仅生成在 build/gate0/reordered，不修改正式源码或改变 canonical 字段语义。

每个执行层均记录 pr_identity（base／merge-base／HEAD 及解析命令）、Python／编译器信息和输入 SHA-256。C++ 编译与运行分别记录 command、exit_code、stdout／stderr；编译／断言失败保留诊断。当前未提交返工的 HEAD 仍是上一轮提交，新候选由输入指纹标识。逐层运行会覆盖 results.json，需要保留时复制到各自 layer-results.json。

Diff 检查默认以 origin/main 为 base，可通过 --base-ref 或 ROSTER_BASE_REF 指定。本脚本解析 base SHA、head SHA、merge-base SHA，检查 merge-base...HEAD 的已提交 PR Diff，并分别检查暂存和工作区 Diff；结果记录每条实际命令、退出码与诊断。不存在／无共同祖先的 base 明确失败。临时隔离 Git 历史回归证明：干净工作区中的已提交空白缺陷仍会失败，修复后通过，未知 base 不会空通过。未提交候选另由源文件指纹标识，当前 HEAD 不冒充未来提交。

边界 CSV 仅是 D4 的预期验收数据，脚本检查其完整性，**未执行年龄筛选引擎**。消费示例证明 DTO 能表达调用，不证明快照失效、事务、预览、打印或 xlsx 输出已实现。g++ 是开发机补充验证，不能替代正式 VS2017 v141_xp、CMake／XMake、Win7 L2/L3 与 R 签认。

维护员需要可重复运行的仓库内检查方法；本脚本不复现也不继承 D1B 原作者的 12/12、8/8 证据。D1B 的检查与静态结果在其返工阶段处理。

2026-10-03，受控需求/规划修订为 v2.1，任务台账 OS 条款同步 SP1 / 6.1.7601；依据 [OD-0002](../../docs/decisions/OD-0002-Windows7-SP1目标基线.md)。只有这三份资料的 BASELINES 指纹更新，业务样表与 ContractVersion 4 不变。脚本成功不等于 Win7 或 Gate 验收通过。
