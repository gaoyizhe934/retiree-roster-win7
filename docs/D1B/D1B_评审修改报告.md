# D1B：按 main ContractVersion 4 基线返工使用流程与模板设计

阶段/轨道：D1B；设计日期2026-10-01，最后修订2026-10-02。唯一有效PR为#3，保持Draft。

main `567d9cd32befc2b8aa7ae99487f8b6d2170f1436` 是当前有效合并基线，CV4 Draft。contract candidate `e8ad944e7c9c8df77c7c5fd883c4459a75270e92` 与 PR2 final review head `f47fa3e251d5fa02f077a6cf9f39feeebf15d3f4` 单独记录；PR2已APPROVE并合并，不等于Gate0通过。

旧设计遗漏了输入枚举数值解耦、FieldChange的有效payload、预检可信边界与派生人数，并默认暴露宽泛筛选和未闭环报告。当前源与产物按CV4重建：

- 导入/编辑都用try_to_person_field显式映射并查FieldSpec，27/28个case可核查，forged/unknown/Unspecified拒绝。
- FieldChange按clear、日期、Text、Enum分状态；clear只接受空value+canonical Unknown；日期赋值有效已知且无文本；姓名禁清空，既有LifeStatus/DeathDate只读，经待批准D20更正。
- P12 caller proposal经服务读源/hash/worksheet/Profile/binding/状态重验，服务保管可信版本与immutable checked copy；Confirm可源字节核对SHA/identity，缺失或变化拒绝，入库不消费重读新内容。
- total_count()仅派生rows.size()；YearCount的空启用与负值均拒绝，shape不冒充完整FilterSpec validator。
- 候选筛选白名单和类型比较；Unknown日期组件空白/disabled；P14/P15报告禁用；P20搜索语义与Q11待A/R。
- 同源生成MD/HTML/JSON；增加可复现反例和只读--check，删除旧验证数字与正式设计的内部流程术语。

本轮CV4提交直接基于上述main，不承接旧#1或双父D1B merge commit。实际提交SHA、merge-base、behind、远程头和真实提交列表，由PR #3正文及提交后发布快照固定。发布前查询确认现有规则仅覆盖main，#3分支无适用保护规则；本轮未修改规则。按用户明确授权更新同一#3，清理旧历史时校验旧远程头并保留原本地工作树；不新建重复PR，不执行合并。分支v3仅为历史名称，内容以CV4为准。

当前验证重算51项静态、14项交付、18项输入核查（基准+17反例），两项回归测试通过；--check逐字节无漂移。2026-10-02完成Codex In-app Browser（UA Chrome/154.0.0.0）1024×768及800×768页面目视，修复长表中文逐字换行并验证键盘/横向滚动；打印CSS已检查，实际分页/实物未测。以当前证据JSON、输入指纹和审核记录为准，不继承历史数量；未运行Win32、导入服务、GDI/xlsx、实物打印或Win7 VM，不代签R。修改文件及每项清单处理见[交付与审核记录](D1B_交付与审核记录.md)。

新#3审查头必须在发布后重新固定并重跑检查；非作者R再走RV01–RV09并提交Formal Review。当前ContractVersion仍Draft，DatabaseSchemaVersion独立未分配，Gate0未通过，甲方/A/C/R剩余条件未完成。
