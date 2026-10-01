# D1B：按PR2契约v3返工使用流程与模板设计

阶段/轨道：D1B。此报告归档原PR1的返工内容；用户在审核材料后明确授权commit、push及prbody更新。按授权更新PR正文，旧正文在本地备份；标题和既有远程分支保留，不另发Comment。

原PR1 HEAD `4a141ede0d3a0d82a647e774cbc4ae6861fed8ed`；返工起点PR2 HEAD `279a204aaf00233fac262f79ac4e3dd80d392f21`。ContractVersion 3 Draft，Gate 0 未通过；DatabaseSchemaVersion独立未分配。发布核对时PR2仍未合并，PR1整合依赖历史不表示PR2获批或Gate冻结。

- 29字段重建为34个PersonFieldId，PersonId/PersonCode/EmployeeNo分离；新增/编辑/导入按能力和输入枚举限制。关怀状态转独立TagMutation，年度慰问不跨年，系统审计只读。
- 导入增加Profile冻结证据与唯一匹配、3处置、ImportFieldId、明确状态、batch_id/preview_revision/source_sha256和版本摘要。确认绑定服务不可变预检，语义变化重新预检，成功revision不重复确认。
- 日期保留四种精度；筛选3场景、显式状态、as_of_date、集合/下限、字段及标签All/Any；Party50不强制在世，删除最大年龄输入。
- 预览/打印/xlsx同snapshot_id和模板值副本，变更后StaleSnapshot；模板4来源与0.1mm整数，签字为BlankSignature、T03编号PersonCode，0自动人数、默认参数均建议。
- 同源重建MD/HTML/控件/Tab/模板和检查JSON，更新Q/RV/README/交接及隐私扫描。原Word/Excel、PR2契约不改。

验证：30/30项静态、12/12项交付检查通过，9/9检查器反例符合预期；当前23页面/共用区、239项控件与展示（224项可操作）、34字段、3模板。详情以三证据JSON为准。内置浏览器拒绝file协议，未完成目视检查；作者结构检查不代替功能或兼容验收。未运行实际Win32/导入/GDI/xlsx/物理打印/Win7 VM，没有L1/L2/L3证据，非作者R未签认，Gate 0继续未通过。

逐项对照和逐文件原因见交付与审核记录。发布前核对远程，保留原PR1历史并整合PR2支撑基线，以普通快进推送更新原PR1及正文。PR2合入main前，PR1的对main差异含依赖基线；不强推、不合并PR，不代签Gate。
