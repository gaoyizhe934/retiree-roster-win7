# D1B 使用流程与模板设计（契约v4）

阶段/轨道：D1B。版本 v0.3；设计日期 2026-10-01，最后修订 2026-10-02。ContractVersion 4 Draft；DatabaseSchemaVersion 独立且尚未分配；Gate 0 未通过，待非作者 R 复核。

当前基线 main `567d9cd32befc2b8aa7ae99487f8b6d2170f1436`；contract candidate `e8ad944e7c9c8df77c7c5fd883c4459a75270e92`；PR2 final review head `f47fa3e251d5fa02f077a6cf9f39feeebf15d3f4`。PR #2 已 APPROVE + merged，PR #3 base 已为 main；PR2 合并不表示 Gate 0 PASS。

- [离线阅读版](D1B_使用流程与模板设计.html)与[设计稿](D1B_使用流程与模板设计.md)：同源页面流转、34字段、Tag、预检、筛选、快照和三模板。
- [交付与审核记录](D1B_交付与审核记录.md)：清单对照、真实 Git 身份、逐文件原因、验证和阻塞。
- [评审修改报告](D1B_评审修改报告.md)：CV4 语义迁移与待审查结论。
- [结构化数据](证据/控件与模板数据.json)、[静态检查](证据/静态核查结果.json)、[交付检查](证据/交付核查结果.json)、[生成器反例](证据/生成器反例核查结果.json)：当前输入重算，不继承历史统计。
- [正文源](生成/设计正文.md)、[数据源](生成/设计数据.json)、[生成器](生成/build_design.py)、[反例及重建测试](生成/test_build_design.py)：Python 3 标准库，无网络构建依赖。

```text
python docs/D1B/生成/build_design.py
python docs/D1B/生成/build_design.py --check
python docs/D1B/生成/test_build_design.py
```

`--check` 只读重建并逐字节比较六份产物；漂移或检查失败返回1，不改写产物。正常构建只在检查全部通过时写出。输入 SHA-256、版本和固定基线见交付 JSON；实际 Git 审查头及提交后验证由 PR #3 和发布快照固定；生成物记录输入指纹，不在提交中内嵌自身 SHA。

ImportFieldId/EditableFieldId 与 PersonFieldId 数值解耦，27/28个字段经 try_to_person_field 显式映射；FieldChange 区分文本、枚举、日期与 canonical Unknown 清空。P12 提案由服务重验，Confirm 源身份核对与 immutable checked copy 入库分离。total_count() 仅由 rows.size() 派生；YearCount validator 只做 shape。

Unknown 日期年月日空白/disabled；P22 既有 LifeStatus/DeathDate 只读，更正经待批准的 D20；P30 筛选白名单/类型比较为候选；P20 搜索语义与 P14/P15 报告接口待 A/R，因此报告导出默认禁用。

D1B 唯一有效 PR 为 [#3](https://github.com/gaoyizhe934/retiree-roster-win7/pull/3)，旧 #1 已关闭。当前远程分支 `docs/d1b-contract-v3-design` 是历史名称，当前设计目标为 CV4；本地 `docs/d1b-contract-v4-design` 直接起于上述 main，CV4 变更统一发布至 #3 的现有远程分支。清理旧 ancestry 时校验旧远程头，旧提交保留在原本地工作树；当前提交 SHA、远程头、真实提交列表与提交后检查见 PR 正文和发布快照。不新建 D1B PR。

权威顺序见[基线说明](../baseline/00_基线与权威来源.md)，正式质量结论见[Gate Status](../status/GATE_STATUS.md)。原始 Word/Excel、main 契约和其他轨道材料保持不变。作者结构和页面检查不代表 Win32、导入事务、GDI/xlsx、实物打印或 Win7 兼容验收。
