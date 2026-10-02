# 导入 Profile 冻结说明

状态：**未冻结**。冻结人、日期、批准证据：均待 A/B/C/R 复核。当前没有可自动使用的已冻结 Profile。

样表 Sheet1 的第 1 行有 52 个非空表头，第 3 行有 23 个，第 23 列为空，第 24 列为备注。同一工作表的两个区域是候选结构，不能默认第 3 行永久代表所有导入格式。

## 候选流程

选择文件与工作表 → 识别已冻结 Profile → 自动预填或映射确认 → 预检 → 明确确认 → 事务入库。

只有表头唯一匹配已冻结 Profile，且无缺失、重复、歧义、顺序变化、未知列时，才允许自动预填并进入预检。其余情况进入映射确认。所有路径都必须预检；预检与取消不写正式 Person。

Profile 需记录 ID、版本、表头行号、列索引／名称／处置、必填条件、枚举与日期解析策略及批准证据。表头行号是具体 Profile 配置，不是全局常量。列索引为 0 起算，行号为 1 起算；空标题仍保留物理位置。

## 状态与重复候选

LifeStatus 不要求源表一定有列，但新建／确认导入前必须解析成 Living 或 Deceased。初始为 Unknown，不自动勾选在世或去世。有有效源列时源列优先；缺失时需要维护员确认批次默认值，或已冻结 Profile 明确给出默认值。明确但非法的源值属于异常，不能被默认值掩盖。

`ImportStatusResolution` 记录来源与回退默认值、确认标志；混合来源用 Mixed，同时保存 Profile／映射版本。服务对完整预检语义生成不透明 preview_revision 并保管不可变的预检结果；ConfirmImportRequest 仅携带 batch_id、preview_revision、confirmed_by 与请求元信息，不再次接收状态、映射或重复处置。

列绑定、mapping/profile version、状态解析、重复候选处置、源文件内容／工作表发生任一变化时，旧 revision 失效，必须重新预检并生成新 revision。source_sha256 由服务计算并记录；确认时校验源身份／内容是否仍与该 revision 相符，源缺失或变化必须拒绝并重新预检。该比对可读取源字节计算摘要，但入库只能使用已检查的数据副本，不能把重读到的新内容或调用方的新语义替换进旧 revision。服务须验证批次与 revision 对应且可确认，成功确认后同一 revision 不可重复入库。该约束是 D3 的实现验收，当前只有 DTO 与编译／结构测试。

未解决重复候选、Unknown 状态、未知／Unsupported 列、缺少姓名、非法日期或枚举均阻断确认。重复候选不能按工号重复直接覆盖档案，初期禁止自动合并；具体候选识别与人工处置规则待 A/R 验证。

## 冻结前必须补齐

- 第二份样表或有代表性的脱敏样本、两区域字段语义与类型。
- Profile 唯一匹配条件、空白／重复标题策略、枚举代码（尤其党员判定）。
- 来源缺失状态的实际业务选择、重复候选的人工处置方式。
- 23 列保留对照及无静默丢失证据；见[字段映射](02_字段映射与数据保留策略.md)。

ImportProfile 不携带可写的 frozen 标志。冻结状态及批准证据来自配置仓储／审批记录，服务按 profile_id 与 version 查询；UI 请求中的标识不是批准证明。当前没有已冻结 Profile；配置仓储校验留给 D3。

ImportColumnBinding 使用只含可导入字段的 ImportFieldId；系统 ID、固定编号、审计字段和拼音键没有可选枚举项。共享 is_valid_import_binding 再校验能力元数据，拒绝强制类型转换伪造的系统字段值。LifeStatus 源列必须显式确认其映射（status_source_confirmed），随后仍须通过状态值解析；不得把任意源列偷偷绑定为状态。服务负责调用该校验，用户布尔值不能替代预检证据。

## D3 不可信提案与可信预检

ImportPreviewRequest 的 column_bindings、status_resolution、mapping_version、profile_id／profile_version 均为调用方候选输入，不是批准证明。只有 Application Service 完成下面全部校验后生成并保存的 ImportPreview 才可供确认；当前头文件的字段白名单／结构函数不是完整服务验证。

| 序号 | D3 强制行为 | 验收结果 |
| --- | --- | --- |
| 1 | 预检由服务重新读取 source_file_path 的源文件，固定本次读取的内容 | 不信任调用方缓存或摘要 |
| 2 | 服务计算源内容 SHA-256 | 保存至可信预检，绑定本次解析内容 |
| 3 | 校验 worksheet 身份与内容 | 不存在／不支持的工作表拒绝 |
| 4 | 从已批准配置校验 profile_id／profile_version | 未批准、未知或伪造版本拒绝；当前未冻结 Profile 不可自动使用 |
| 5 | 逐项校验 ImportColumnBinding、物理列身份、白名单和能力 | 用 try_to_person_field 显式映射，拒绝无效或系统专管目标 |
| 6 | 检查无重复 Person target | 不允许多源列静默覆盖同一字段 |
| 7 | 检查 Unknown／Unsupported 列及处置 | 未解决则预检失败；BatchRawOnly 仅保存在私有批次原值 |
| 8 | 校验 LifeStatus 来源、确认证据和实际值 | 用户布尔值不替代证据，Unknown／非法状态阻断 |
| 9 | 服务从已校验映射生成 mapping_version | 调用方版本仅为提案；伪造版本拒绝或由服务重建 |
| 10 | 服务生成不透明 PreviewRevision | 绑定源、工作表、Profile、映射、状态和重复处置 |
| 11 | 服务保存不可变 ImportPreview 与可入库数据副本 | 未通过预检不得生成可确认对象 |
| 12 | Confirm 仅按 (batch_id, preview_revision) 读取保存结果 | 不存在、错配、已失效或不可确认结果拒绝 |
| 13 | Confirm 不重新接收／解释调用方映射和状态语义 | 只消费服务已验证的 revision |
| 14 | 同一 revision 不得二次写入 | 再次确认拒绝或按批准的幂等策略返回原结果；策略待 D3 冻结 |
| 15 | 源内容变化必须重新预检 | Confirm 核对服务保存的源身份与摘要，变化拒绝；映射／Profile 等变化也使旧 revision 失效 |

D3 集成必须覆盖：伪造 profile_version 拒绝、伪造 mapping_version 重建／拒绝、重复 target 拒绝、未确认状态源拒绝、预检后文件变化导致 Confirm 拒绝、revision 不存在拒绝、batch/revision 错配拒绝、修改映射后旧 revision 拒绝、二次 Confirm 按冻结策略处理。还须验证摘要对应入库副本、源缺失失败和事务内至多一次写入。这些用例尚未运行；R02 在 #2 只完成信任边界与验收责任说明，不宣称服务风险已消除。
