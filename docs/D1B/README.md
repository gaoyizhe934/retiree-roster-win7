# D1B 使用流程与模板设计（契约v3返工）

阶段/轨道：D1B。版本v0.2，ContractVersion 3 Draft；Gate 0 未通过，非作者R未签认。DatabaseSchemaVersion独立且尚未分配。

- [离线阅读版](D1B_使用流程与模板设计.html)：九章同源内容，内嵌SVG、无外部运行资源。
- [设计稿](D1B_使用流程与模板设计.md)：34个PersonFieldId能力、独立Tag区、Profile/列处置/preview_revision、FilterSpec、snapshot_id及三模板。
- [交付与审核记录](D1B_交付与审核记录.md)：清单逐项对照、验证和限制。
- [评审修改报告](D1B_评审修改报告.md)：归档本轮修改；PR正文按用户明确授权同步更新，未另发Comment。
- [结构化数据](证据/控件与模板数据.json)、[静态检查](证据/静态核查结果.json)、[交付检查](证据/交付核查结果.json)：当前版本数据，统计从生成器计算。
- [正文源](生成/设计正文.md)、[控件与模板源](生成/设计数据.json)、[生成及检查脚本](生成/build_design.py)：随材料保存，Python3标准库离线重建，仅读契约与原始资料、重建本目录产物。

```text
python docs/D1B/生成/build_design.py
```

当前没有已冻结Profile。27个可导入业务字段与28个可编辑字段受ImportFieldId/EditableFieldId和能力元数据限制；系统ID、固定编号、审计字段不可由调用方填写，拼音键不可导入。FullName是唯一导入必填元数据项；LifeStatus仍须明确解析。Tag独立请求、年度慰问绑定适用年，日期保留精度。

FilterSpec支持三场景、显式状态、集合或下限、字段和标签各自All/Any；六首页入口只是UI预设，Party50不强制在世。三输出消费同snapshot_id和模板值副本，StaleSnapshot回筛选重生成。内部物理尺寸为0.1mm整数；模板参数为建议，硬边距、字号与xlsx转换待D5。

返工起点为PR2 `279a204aaf00233fac262f79ac4e3dd80d392f21`，对照原PR1 `4a141ede0d3a0d82a647e774cbc4ae6861fed8ed`。两PR读取时均未合并；PR2和Proposed ADR不是批准基线。权威规则见[基线说明](../baseline/00_基线与权威来源.md)，正式结论见[Gate Status](../status/GATE_STATUS.md)。

新分支遵守[GitHub协作命名规范](../../GitHub协作命名规范.md)与[OD-0001](../decisions/OD-0001-分支命名规则.md)：仅ASCII，类型/小写英文主题。PR1既有中文分支不擅自改名。用户已明确授权本轮commit、push和prbody更新；旧PR正文在本地备份，按授权同步正文。原v0.1由原PR1提交追溯；当前目录均以v0.2为准，原始Word/Excel不改。

作者检查仅验证静态设计，不代表Win32、导入、GDI/xlsx或Win7兼容验收。非作者R按RV01–RV09复核，甲方/A/C待办见Q01–Q13。
