# OD-0002 受控基线 OOXML 语义差异

Decision：[OD-0002](../../decisions/OD-0002-Windows7-SP1目标基线.md)。Pre-SP1 baseline anchor：`567d9cd32befc2b8aa7ae99487f8b6d2170f1436`。该 SHA 是修订前不可变锚点，不是当前 main 或本文件所属提交的声明。

本证据绑定下列六个文件内容 SHA-256，记录 v2.0 → v2.1 / SP1 的固定差异。承载 PR 为 [#8](https://github.com/gaoyizhe934/retiree-roster-win7/pull/8)；其 review_head、base、merge-base 与 Formal Review 身份以 GitHub 平台记录为准，本文件不复制当前 HEAD。

## 文件内容身份

| 文件 | 修订前 SHA-256 | 修订后 SHA-256 |
| --- | --- | --- |
| docs/退休人员名册打印小程序需求说明.docx | 658b10952e2cba734990d2b37f862b2495196e51427c117cf2a4edde7992c641 | 7c0240282586690886fef84e20d42f6f5c800acae952d9b23697135909a152bb |
| docs/退休人员名册打印小程序开发规划.docx | c1caac2094c6778363b27af2011af3cd0118fa4e96e570761479247748d347c1 | 241e550d9c3c4de85342f4aa064833409ce79acbe940a0e29078d23599f90d72 |
| reference/七阶段开发任务清单.xlsx | 7648e936d249f817bc61d43bcf109eafc94802b9a1dfd370fd23cdb45d802e26 | dc4002bef4f7d8f4084536ede7e16f6072b63facaa12e5263694391e39c46b80 |

旧内容直接以 Git bytes stdout 读取 `git show <anchor>:<path>`，未使用 Windows PowerShell 文本重定向。新内容只读当前工作树；复核脚本先校验文件指纹，再比较解压 entry 的完整字节及 SHA-256。这里的 BYTE_IDENTICAL 指 ZIP entry 解压内容，压缩包整体指纹已在上表绑定。

## ZIP entry 差异

| 文件 | 旧/新 entry 集合及顺序 | entry 总数 | 变更 entry | 其它 entry |
| --- | --- | --- | --- | --- |
| docs/退休人员名册打印小程序需求说明.docx | YES / 相同 | 27 | word/document.xml | 26 个 BYTE_IDENTICAL |
| docs/退休人员名册打印小程序开发规划.docx | YES / 相同 | 19 | word/document.xml | 18 个 BYTE_IDENTICAL |
| reference/七阶段开发任务清单.xlsx | YES / 相同 | 17 | xl/worksheets/sheet1.xml<br>xl/worksheets/sheet2.xml<br>xl/worksheets/sheet3.xml | 14 个 BYTE_IDENTICAL |

全部发生变化的解压 entry 指纹如下；其它 entry 逐字节相等（包含 Word 样式、编号、关系、文档属性，以及 Excel workbook、样式、关系与第4张技术债工作表）。

| 文件 | Entry | 旧 entry SHA-256 | 新 entry SHA-256 |
| --- | --- | --- | --- |
| docs/退休人员名册打印小程序需求说明.docx | word/document.xml | 67f0768baa25183a16db7dbcdf967716dc74800c8d9a5cf27095c131ff54173c | bc064a8f04ab8b143266ec16c116187c93da3d1eae89209fe1727af87874e06a |
| docs/退休人员名册打印小程序开发规划.docx | word/document.xml | 9062f0a48dc317914346efd82f4cd68dab1d0df95f650394c8306991090d6651 | d43a4903f8e2e6d8c7f82fb3928d9e83097fd73bb7bb1d65c31cbbdd75a45b08 |
| reference/七阶段开发任务清单.xlsx | xl/worksheets/sheet1.xml | 15025e3c44428ab7f966802845a105783d64f03a4d511491b82ef136f5638f08 | 6ecebd637a674f36ea622ce6560d69f3ef0a24042f338bc9bb6d6267bd594e66 |
| reference/七阶段开发任务清单.xlsx | xl/worksheets/sheet2.xml | 7e0a20ed4125becc45e461c3eb8b0056a2cbaa06398f7e4848bd437117403c4b | 2ce9a363de176ae2165e2df8325ac0062f68be29d9f9e0f6ccc2e275dd1ef527 |
| reference/七阶段开发任务清单.xlsx | xl/worksheets/sheet3.xml | 57a82f4ee2ec109ad21a629c82742db11a30b766be497b956b39a99005b31027 | 043a912958da19b826e4d41cdafd5470fa547df5616514f3b57b5e7d92446a4f |

## Word 完整文本差异

定位采用 `word/document.xml` 中按文档顺序枚举的全部 `w:p`（包含表格单元格内段落），从1开始计数，不是页码；`w:t` 编号是在该段落内部从1枚举。以下覆盖所有改变的文本节点：每个改变的原有段落均仅有 `w:t[1]` 改变，表中旧/新文本是该节点完整文本，也等于完整段落文本。原有段落没有新增/删除 run 或其它 XML 节点。

### 需求说明

原有段落 217 个，修订后 220 个；改变原有段落 9 个，另在末尾增加3个修订记录段落。

| 段落/文本定位 | 旧文本 | 新文本 | 类型 |
| --- | --- | --- | --- |
| w:p[9] / w:t[1] | 原生离线  静态依赖  Windows 7 RTM 验证  门禁式交付 | 原生离线  静态依赖  Windows 7 SP1 验证  门禁式交付 | OS |
| w:p[13] / w:t[1] | v2.0 | v2.1（SP1 修订，2026-10-03） | revision |
| w:p[21] / w:t[1] | Windows 7 RTM 6.1.7600，32 位主发行包；VirtualBox 纯净虚拟机验证 | Windows 7 SP1 6.1.7601，32 位主发行包；VirtualBox 纯净虚拟机验证 | OS |
| w:p[28] / w:t[1] | 本项目交付一个单机离线的 Windows 桌面程序。维护人员导入现有 Excel 人员表后，可维护人员档案、按业务条件生成名单、生成可直接打印的 Excel，并在未安装 Microsoft Excel 的计算机上完成导出和本机打印。程序以 32 位原生可执行文件为主发行包，必须在 Windows 7 RTM 32 位和 64 位纯净虚拟机中通过启动、导入、筛选、导出、预览、打印和恢复验证。 | 本项目交付一个单机离线的 Windows 桌面程序。维护人员导入现有 Excel 人员表后，可维护人员档案、按业务条件生成名单、生成可直接打印的 Excel，并在未安装 Microsoft Excel 的计算机上完成导出和本机打印。程序以 32 位原生可执行文件为主发行包，必须在 Windows 7 SP1 32 位和 64 位纯净虚拟机中通过启动、导入、筛选、导出、预览、打印和恢复验证。 | OS |
| w:p[176] / w:t[1] | 6 Windows 7 RTM 与 VirtualBox 验证基线 | 6 Windows 7 SP1 与 VirtualBox 验证基线 | OS |
| w:p[181] / w:t[1] | VirtualBox 中 Windows 7 RTM 32 位 6.1.7600；无 SP1、无 Office、无 .NET、无 VC++ Redistributable。 | VirtualBox 中 Windows 7 SP1 32 位 6.1.7601；已安装 SP1、无 Office、无 .NET、无 VC++ Redistributable。 | OS |
| w:p[184] / w:t[1] | VirtualBox 中 Windows 7 RTM 64 位 6.1.7600；同样保持无额外运行库。 | VirtualBox 中 Windows 7 SP1 64 位 6.1.7601；同样保持无额外运行库。 | OS |
| w:p[193] / w:t[1] | L0：开发机编译、单元测试、静态依赖检查。L1：开发机端到端脱敏样表测试。L2：Win7 RTM 两台虚拟机真实启动、导入、筛选、导出、预览、打印和恢复。L3：从 00_Base 恢复后的纯净发布回归。 | L0：开发机编译、单元测试、静态依赖检查。L1：开发机端到端脱敏样表测试。L2：Win7 SP1 两台虚拟机真实启动、导入、筛选、导出、预览、打印和恢复。L3：从 00_Base 恢复后的纯净发布回归。 | OS |
| w:p[199] / w:t[1] | 32 位候选包在 Win7 RTM 32/64 位启动，无缺 DLL、API 或运行库错误。 | 32 位候选包在 Win7 SP1 32/64 位启动，无缺 DLL、API 或运行库错误。 | OS |
| w:p[218]（新增） | — | Windows 7 目标基线修订记录 | revision |
| w:p[219]（新增） | — | 2026-10-03，依据 OD-0002，目标环境由 Windows 7 RTM 6.1.7600 修订为 Windows 7 SP1 6.1.7601，覆盖 x86 与 x64。原 v2.0 为历史基线，可从 Git 历史复核。 | revision |
| w:p[220]（新增） | — | 32 位主发行包、C++14、静态依赖和 WINVER/_WIN32_WINNT=0x0601 保持不变。虚拟机不得额外安装 Office、.NET 或 VC++ Redistributable。未新增 Windows Edition 限制，本修订不代表 Gate 0 通过。完整决定见 docs/decisions/OD-0002-Windows7-SP1目标基线.md。 | revision |

### 开发规划

原有段落 353 个，修订后 356 个；改变原有段落 12 个，另在末尾增加3个修订记录段落。

| 段落/文本定位 | 旧文本 | 新文本 | 类型 |
| --- | --- | --- | --- |
| w:p[9] / w:t[1] | 原生离线  静态依赖  Windows 7 RTM 验证  门禁式交付 | 原生离线  静态依赖  Windows 7 SP1 验证  门禁式交付 | OS |
| w:p[13] / w:t[1] | v2.0 | v2.1（SP1 修订，2026-10-03） | revision |
| w:p[21] / w:t[1] | Windows 7 RTM 6.1.7600，32 位主发行包；VirtualBox 纯净虚拟机验证 | Windows 7 SP1 6.1.7601，32 位主发行包；VirtualBox 纯净虚拟机验证 | OS |
| w:p[111] / w:t[1] | 所有轨道使用同一 C++14 契约和目录边界；候选包在 Win7 RTM 至少能启动空界面。 | 所有轨道使用同一 C++14 契约和目录边界；候选包在 Win7 SP1 至少能启动空界面。 | OS |
| w:p[127] / w:t[1] | 端到端链路在 Win7 RTM 两台虚拟机通过；P0/P1 为零才可进入试运行。 | 端到端链路在 Win7 SP1 两台虚拟机通过；P0/P1 为零才可进入试运行。 | OS |
| w:p[149] / w:t[1] | 安装 Visual Studio 2017 v141_xp、CMake 3.15 和 XMake 2.9.x 开发环境。创建 Win7 RTM 32/64 位 VirtualBox 虚拟机、00_Base 快照和脱敏样表传入路径。 | 安装 Visual Studio 2017 v141_xp、CMake 3.15 和 XMake 2.9.x 开发环境。创建 Win7 SP1 32/64 位 VirtualBox 虚拟机、00_Base 快照和脱敏样表传入路径。 | OS |
| w:p[158] / w:t[1] | 所有轨道使用同一 C++14 契约和目录边界；候选包在 Win7 RTM 至少能启动空界面。 | 所有轨道使用同一 C++14 契约和目录边界；候选包在 Win7 SP1 至少能启动空界面。 | OS |
| w:p[173] / w:t[1] | 两套可复现命令、配置对照、依赖检查结果、CMake 候选空程序 Win7 RTM 启动证据。 | 两套可复现命令、配置对照、依赖检查结果、CMake 候选空程序 Win7 SP1 启动证据。 | OS |
| w:p[250] / w:t[1] | 端到端链路在 Win7 RTM 两台虚拟机通过；P0/P1 为零才可进入试运行。 | 端到端链路在 Win7 SP1 两台虚拟机通过；P0/P1 为零才可进入试运行。 | OS |
| w:p[295] / w:t[1] | 6 Windows 7 RTM VirtualBox 测试 SOP | 6 Windows 7 SP1 VirtualBox 测试 SOP | OS |
| w:p[302] / w:t[1] | 创建 Win7 RTM x86 与 x64 来宾，确认 build 7600；不安装 SP1、Office、.NET 或 VC++ Redistributable。 | 创建 Win7 SP1 x86 与 x64 来宾，确认 build 7601；已安装 SP1；不安装 Office、.NET 或 VC++ Redistributable。 | OS |
| w:p[348] / w:t[1] | L0/L1 通过；两台 Win7 RTM VM 完成 L2；00_Base 回归完成 L3。 | L0/L1 通过；两台 Win7 SP1 VM 完成 L2；00_Base 回归完成 L3。 | OS |
| w:p[354]（新增） | — | Windows 7 目标基线修订记录 | revision |
| w:p[355]（新增） | — | 2026-10-03，依据 OD-0002，目标环境由 Windows 7 RTM 6.1.7600 修订为 Windows 7 SP1 6.1.7601，覆盖 x86 与 x64。原 v2.0 为历史基线，可从 Git 历史复核。 | revision |
| w:p[356]（新增） | — | 32 位主发行包、C++14、静态依赖和 WINVER/_WIN32_WINNT=0x0601 保持不变。虚拟机不得额外安装 Office、.NET 或 VC++ Redistributable。未新增 Windows Edition 限制，本修订不代表 Gate 0 通过。完整决定见 docs/decisions/OD-0002-Windows7-SP1目标基线.md。 | revision |

### Word 结构与业务边界

逐个 XML 文本节点仅允许上表 OS 词组替换及 v2.0 → v2.1 修订标记；从新 XML 副本移除表列的3个末尾修订段落后，与按允许规则规范化的旧 XML 完整比较，结果相同。对照是在内存中进行，未重新保存 DOCX。因此原有 pPr/rPr、表格、页布局/节设置及其它非授权 XML 变化为0；其它 ZIP entry 亦逐字节不变。

由以上穷尽文本差异及全树对照可核验：R01–R05 业务规则、字段模型、打印业务要求、A/B/C/R 职责均未变化（除目标 OS 环境条款）；C++14、Win32/x86 主发行包、静态依赖及 0x0601 未变化。含导入/打印动作的变更段落只替换其 OS 环境名称，不修改业务动作或验收责任。

## XLSX 完整单元格差异

`xl/workbook.xml` 的四张表及顺序为：施工台账、每日 Gate、接口与证据、技术债登记；该 entry 与其关系 entry 均 BYTE_IDENTICAL。实际变化仅在前三张表对应的 sheet1.xml / sheet2.xml / sheet3.xml；技术债登记的 sheet4.xml BYTE_IDENTICAL。

| Sheet | Cell | 旧值 | 新值 | Style ID 旧/新 | Formula 旧/新 |
| --- | --- | --- | --- | --- | --- |
| 施工台账 | D5 | Win7 RTM x86/x64 纯净 VM 通过 L3 | Win7 SP1 x86/x64 纯净 VM 通过 L3 | 8 / 8 | none / none |
| 施工台账 | E11 | 安装 VS2017 v141_xp、CMake 3.15、XMake 2.9.x；创建 Win7 RTM 6.1.7600 x86、x64 VirtualBox VM；确认无 SP1、无 VC++ 运行库、无 Office，并建立 00_Base。 | 安装 VS2017 v141_xp、CMake 3.15、XMake 2.9.x；创建 Win7 SP1 6.1.7601 x86、x64 VirtualBox VM；确认 SP1 基线、无 VC++ 运行库、无 Office，并建立 00_Base。 | 8 / 8 | none / none |
| 施工台账 | F15 | CMake/XMake 命令与配置对照、32 位 CMake 候选 exe、依赖检查、两台 Win7 RTM VM 启动证据。 | CMake/XMake 命令与配置对照、32 位 CMake 候选 exe、依赖检查、两台 Win7 SP1 VM 启动证据。 | 18 / 18 | none / none |
| 施工台账 | K31 | L3：Win7 RTM x86/x64 | L3：Win7 SP1 x86/x64 | 18 / 18 | none / none |
| 每日 Gate | B17 | Win7 RTM VM | Win7 SP1 VM | 8 / 8 | none / none |
| 每日 Gate | B18 | 00_Base 恢复后的 Win7 RTM x86/x64 VM | 00_Base 恢复后的 Win7 SP1 x86/x64 VM | 8 / 8 | none / none |
| 每日 Gate | D7 | Win32 Release 空程序在 Win7 RTM x86/x64 均启动；接口 v1 冻结 | Win32 Release 空程序在 Win7 SP1 x86/x64 均启动；接口 v1 冻结 | 8 / 8 | none / none |
| 每日 Gate | E6 | 两台 VM 基线；无 SP1/Office/VC++ 运行库 | 两台 VM 基线；SP1 6.1.7601；无 Office/VC++ 运行库 | 8 / 8 | none / none |
| 接口与证据 | F19 | Win7 RTM x86/x64 L3 | Win7 SP1 x86/x64 L3 | 8 / 8 | none / none |

实际结果：changed_cells = 9；style_changed_cells = 0；formula_changed_cells = 0；merged_range_changes = 0；sheet_structure_changes = 0。

九格的原始类型均为 `t="str"`，只变 `v` 文本，style id 与 formula 节点保持原值。复核每张表的 cell reference 集合一致；在新 XML 副本将这九格 `v` 恢复旧值后，整张 worksheet XML 树与旧树完全相同，覆盖行列结构/尺寸、视图/冻结窗格、合并区域、样式引用、公式及全部其它单元格。配合其余14个 entry 逐字节不变，可核验无其它工作表结构、样式、公式、进度、Gate 结论或技术债变化；“通过 L3”等任务要求原文保留，不作为实际完成声明。

## 独立复核方法与实际命令

本轮作者实际执行：

```powershell
# 在仓库根目录执行；本地脚本副本仅作为辅助文件。
$env:PYTHONIOENCODING = 'utf-8'
& 'C:/Users/高翌哲/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' 'D:/退休干部清单/辅助生成文件/SP1/verify_sp1_ooxml.py'
```

退出码0；结果为上列固定文件身份、entry 指纹、21个改变的原有 Word 段落（需求9 / 规划12）、每份3个新增修订段落及9个 Excel 单元格。下方提供该只读脚本的完整副本，Reviewer 不依赖作者机器路径、忽略目录或第三方库：复制到任意临时 `verify_sp1_ooxml.py`，在包含该锚点的仓库根目录执行 `python <临时脚本路径>`，Python 3 标准库与 Git 即可复现。失败返回非零，不写二进制文件。

这是固定证据的独立抽查配方，不接入 Gate0 runner，不增加其检查数量。文件指纹不符时须调查或另行建立受控修订，不能静默重写本证据中的 SHA。

```python
"""Read-only, standard-library reproduction of OD-0002's fixed binary delta."""
from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
from copy import deepcopy
import hashlib
import json
import subprocess
import xml.etree.ElementTree as ET

ANCHOR = '567d9cd32befc2b8aa7ae99487f8b6d2170f1436'
FILES = {
    'docs/退休人员名册打印小程序需求说明.docx': (
        '658b10952e2cba734990d2b37f862b2495196e51427c117cf2a4edde7992c641',
        '7c0240282586690886fef84e20d42f6f5c800acae952d9b23697135909a152bb'),
    'docs/退休人员名册打印小程序开发规划.docx': (
        'c1caac2094c6778363b27af2011af3cd0118fa4e96e570761479247748d347c1',
        '241e550d9c3c4de85342f4aa064833409ce79acbe940a0e29078d23599f90d72'),
    'reference/七阶段开发任务清单.xlsx': (
        '7648e936d249f817bc61d43bcf109eafc94802b9a1dfd370fd23cdb45d802e26',
        'dc4002bef4f7d8f4084536ede7e16f6072b63facaa12e5263694391e39c46b80'),
}
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
X = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
REPLACEMENTS = (
    ('Windows 7 RTM', 'Windows 7 SP1'), ('Win7 RTM', 'Win7 SP1'),
    ('6.1.7600', '6.1.7601'), ('build 7600', 'build 7601'),
    ('无 SP1、', '已安装 SP1、'), ('不安装 SP1、', '已安装 SP1；不安装 '),
)
EXPECTED_CELLS = {
    'xl/worksheets/sheet1.xml': {'D5', 'E11', 'F15', 'K31'},
    'xl/worksheets/sheet2.xml': {'E6', 'D7', 'B17', 'B18'},
    'xl/worksheets/sheet3.xml': {'F19'},
}


def xml_bytes(element):
    return ET.tostring(element, encoding='utf-8')


def paragraph_text(element):
    return ''.join(t.text or '' for t in element.iter(W + 't'))


def transform(text):
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    return 'v2.1（SP1 修订，2026-10-03）' if text == 'v2.0' else text


def verify(root):
    root = Path(root).resolve()
    report = {'anchor': ANCHOR, 'files': []}
    for path, (old_hash, new_hash) in FILES.items():
        # Capture stdout as bytes; do not redirect binary git output in Windows PowerShell.
        old = subprocess.check_output(
            ['git', '-c', 'safe.directory=' + root.as_posix(), 'show', ANCHOR + ':' + path], cwd=root)
        new = (root / path).read_bytes()
        assert hashlib.sha256(old).hexdigest() == old_hash, path
        assert hashlib.sha256(new).hexdigest() == new_hash, path
        with ZipFile(BytesIO(old)) as before, ZipFile(BytesIO(new)) as after:
            assert before.namelist() == after.namelist(), path
            assert len(before.namelist()) == len(set(before.namelist())), path
            changed = [entry for entry in before.namelist() if before.read(entry) != after.read(entry)]
            entries = [{'entry': entry,
                        'old_sha256': hashlib.sha256(before.read(entry)).hexdigest(),
                        'new_sha256': hashlib.sha256(after.read(entry)).hexdigest()}
                       for entry in changed]
            item = {'path': path, 'old_sha256': old_hash, 'new_sha256': new_hash,
                    'zip_entry_count': len(before.namelist()), 'changed_entries': entries,
                    'unchanged_entries': len(before.namelist()) - len(changed)}
            if path.endswith('.docx'):
                assert changed == ['word/document.xml'], path
                a = ET.fromstring(before.read(changed[0]))
                b = ET.fromstring(after.read(changed[0]))
                ps, qs = list(a.iter(W + 'p')), list(b.iter(W + 'p'))
                assert len(qs) == len(ps) + 3, path
                item.update(existing_paragraphs=len(ps), new_paragraphs=len(qs), paragraphs=[])
                normalized_old = deepcopy(a)
                for t in normalized_old.iter(W + 't'):
                    t.text = transform(t.text or '')
                for index, (p, q) in enumerate(zip(ps, qs), 1):
                    ts, us = list(p.iter(W + 't')), list(q.iter(W + 't'))
                    assert len(ts) == len(us), (path, index)
                    runs = [{'text_index': j, 'old': t.text or '', 'new': u.text or ''}
                            for j, (t, u) in enumerate(zip(ts, us), 1) if t.text != u.text]
                    if runs:
                        item['paragraphs'].append({'paragraph': index, 'old': paragraph_text(p),
                                                   'new': paragraph_text(q), 'text_nodes': runs,
                                                   'type': 'revision' if paragraph_text(p) == 'v2.0' else 'OS'})
                normalized_new = deepcopy(b)
                nps = list(normalized_new.iter(W + 'p'))
                parents = {child: parent for parent in normalized_new.iter() for child in parent}
                item['added_paragraphs'] = []
                for index, p in enumerate(nps[len(ps):], len(ps) + 1):
                    item['added_paragraphs'].append({'paragraph': index, 'text': paragraph_text(p)})
                    parents[p].remove(p)
                assert xml_bytes(normalized_old) == xml_bytes(normalized_new), path
                item['non_authorized_XML_changes'] = 0
            else:
                assert set(changed) == set(EXPECTED_CELLS), path
                workbook = ET.fromstring(before.read('xl/workbook.xml'))
                sheet_names = [sheet.attrib['name'] for sheet in workbook.iter(X + 'sheet')]
                item.update(sheet_names=sheet_names, cells=[])
                for entry, expected in EXPECTED_CELLS.items():
                    a, b = ET.fromstring(before.read(entry)), ET.fromstring(after.read(entry))
                    ac = {c.attrib['r']: c for c in a.iter(X + 'c')}
                    bc = {c.attrib['r']: c for c in b.iter(X + 'c')}
                    assert ac.keys() == bc.keys(), entry
                    actual = {ref for ref in ac if xml_bytes(ac[ref]) != xml_bytes(bc[ref])}
                    assert actual == expected, (entry, actual)
                    normalized = deepcopy(b)
                    nc = {c.attrib['r']: c for c in normalized.iter(X + 'c')}
                    sheet_index = int(entry.split('sheet')[-1].split('.')[0]) - 1
                    for ref in sorted(actual):
                        p, q = ac[ref], bc[ref]
                        assert p.attrib.get('t') == q.attrib.get('t') == 'str', ref
                        assert p.attrib.get('s') == q.attrib.get('s'), ref
                        assert p.find(X + 'f') is None and q.find(X + 'f') is None, ref
                        old_value, new_value = p.find(X + 'v').text, q.find(X + 'v').text
                        item['cells'].append({'sheet': sheet_names[sheet_index], 'entry': entry, 'cell': ref,
                                              'old': old_value, 'new': new_value,
                                              'old_style': p.attrib.get('s', '0'), 'new_style': q.attrib.get('s', '0'),
                                              'old_formula': None, 'new_formula': None})
                        nc[ref].find(X + 'v').text = old_value
                    # All worksheet attributes, views, cells, styles, formulas and merges must match.
                    assert xml_bytes(a) == xml_bytes(normalized), entry
                assert len(item['cells']) == 9
                item.update(changed_cells=9, style_changed_cells=0, formula_changed_cells=0,
                            merged_range_changes=0, sheet_structure_changes=0)
            report['files'].append(item)
    return report


if __name__ == '__main__':
    print(json.dumps(verify(Path.cwd()), ensure_ascii=False, indent=2))
```

## 验证边界

本证据仅证明这三份受控文件的固定内容差异及 OOXML 结构约束，不是非作者 Formal Review 或独立 CI，不证明正式 MSVC/v141_xp、CMake/XMake、Win7 L2/L3、Guest 纯净性、产品导入/服务/筛选、GDI/xlsx 或实物打印通过，也不构成 Gate 0 PASS。各责任继续按阶段 PR 与 R 流程验收。
