# D1B v0.3 交付与人工审核记录

设计日期：2026-10-01；最后修订：2026-10-02。阶段 D1B；ContractVersion 4 Draft；DatabaseSchemaVersion 独立且尚未分配；Gate 0 未通过，非作者 R 对本轮材料未签认。

## 当前基线、Git 身份与发布边界

| 身份 | 已核验状态 |
| --- | --- |
| base/main | 567d9cd32befc2b8aa7ae99487f8b6d2170f1436 |
| contract candidate | e8ad944e7c9c8df77c7c5fd883c4459a75270e92 |
| PR2 final review head | f47fa3e251d5fa02f077a6cf9f39feeebf15d3f4；PR2 已 APPROVED + merged，不等于 Gate 0 PASS |
| D1B 唯一 PR | [#3](https://github.com/gaoyizhe934/retiree-roster-win7/pull/3)；Open/Draft，base=main；远程分支 docs/d1b-contract-v3-design 是历史名称，设计内容以 CV4 为准 |
| CV4 历史与审查头 | 本地 docs/d1b-contract-v4-design 从上述 main 起步，D1B 提交仅修改 docs/D1B/**；实际提交 SHA、merge-base、behind、提交列表及远程头由 PR 正文和发布快照固定，不在提交内嵌自身 SHA |
| 旧发布身份 | e15c3dd7a7fe1d52c86c6b8aff09c8db2c4e2818 保留于原本地 PR3 工作树；旧 #1 及双父 D1B merge commit 不纳入本轮 CV4 历史 |

已执行 fetch 和现有分支的 pull --ff-only；原主工作区的未跟踪 CONTEXT/ADR/目录说明保留。当前 main 已获取到本地，本轮 CV4 从该基线创建，提交后检查 merge-base、behind 与旧 #1 ancestry；没有在旧 CV3 ancestry 上追加普通修复，也没有本地分支合并。

2026-10-02 发布前重新查询 GitHub：现有规则仅覆盖 main，#3 分支 protected=false，适用规则为空。本轮没有修改保护规则。按用户对 commit、push、PR 正文及评论的明确授权，将 clean CV4 提交发布到 #3 的同一远程分支；替换旧 ancestry 时使用精确旧头校验，保留原本地提交可恢复。实际执行结果与提交后检查记录在发布快照和 PR 评论中；不关闭重建 PR、不新建额外 D1B PR，不执行合并。分支名中的 v3 仅为历史名称。

## 清单逐项对照

| 清单项 | 实际处理与证据 | 验收边界 |
| --- | --- | --- |
| P0-01/P0-02 | 从当前 main 起草 clean 本地候选；本地无旧 #1 ancestry，behind=0 | 实际远程头及历史检查见发布快照/PR；非作者评审未完成 |
| P0-03 | 本地 ASCII v4 候选；正文说明远程 v3 为历史名称 | 未擅自改名远程分支 |
| 全量 CV4/main | 正文、README、交接、报告和同源产物更新；三种 SHA 身份分开 | CV4仍Draft，Gate0未通过 |
| Import/Edit mapping | 27/28个显式case与Unspecified/default/nullptr核查；P12/P22/RV同步 | C++运行与D3业务服务未代验 |
| FieldChange | §3.3状态表，清空/Date/Text/Enum payload、禁止Identifier/Timestamp；姓名禁清空 | shape不代替D3必填/状态值域 |
| 预检信任边界 | caller proposal重验、可信mapping_version、immutable checked copy；P12/P13/D10/RV02/Q03 | Confirm可源字节hash核对；缺失/变化拒绝，不替换checked copy |
| total_count() | 无可写人数；P30/P40/P50/RV07/Q07同步 | 人数唯一来源rows.size() |
| YearCount | age/party均shape，空启用/负值反例；disabled不筛选 | 完整FilterSpec仍待D4 |
| UI白名单 | 数据源filterable_fields、类型Comparison候选；系统/敏感/编号/工号排除 | 待A/R批准；Date范围未开放 |
| Unknown日期 | 18个Person年月日组件+3个D20组件空白/disabled | DTO内部0；精度启用和Tab规则同步 |
| 状态日期单入口 | 既有LifeStatus/DeathDate P22只读；D20默认禁用至Q04批准 | 新建业务校验；清空/回在世/备份/历史待A/R |
| 报告/搜索 | P14/P15导出禁用；Q11列方式、格式、ExportLog、脱敏；P20标候选语义 | B未新增正式公共接口 |
| 可复现性 | 新静态/交付检查；仓库反例脚本及JSON；--check漂移不写入测试 | 不继承旧30/12/9统计 |
| 页面目视 | 见下方当前轮记录 | 结构parser不代替目视；Win32/Win7实测仍未运行 |
| 文档清理 | 删除内部技能术语；设计日期与最后修订分开 | 工作流程细节只保留在交接与发布边界 |

## 逐文件修改原因

| 文件 | 修改原因 |
| --- | --- |
| 生成/设计正文.md | CV4/main、显式映射、FieldChange、信任边界、派生人数、YearCount、白名单、Q/RV |
| 生成/设计数据.json | 候选白名单/类型比较、姓名及状态日期UI override、报告/搜索/日期默认 |
| 生成/build_design.py | 分离三基线身份、当前header SHA、CV4检查、UI override、只读--check |
| 生成/test_build_design.py | 故意损坏输入反例；独立临时副本验证正常重建和漂移检测不写入 |
| D1B_使用流程与模板设计.md/.html | 从当前源完整重建；HTML标题与CV4状态同步 |
| 证据/控件与模板数据.json | 当前字段/控件/Tab/模板及UI限制同源重算 |
| 证据/静态核查结果.json | CV4新检查、原始资料/契约指纹、模板算术 |
| 证据/交付核查结果.json | 结构/隐私、当前输入指纹与外部审查头定位 |
| 证据/生成器反例核查结果.json | 当前生成器反例结果随仓库可复现 |
| README/本记录/评审修改报告 | main与PR2最新状态、真实基线、发布方式和复核入口 |

所有候选差异仅 docs/D1B/**，不修改程序契约、原始 Word/Excel、Gate状态或其他轨道文件。测试结果、命令退出码、逐文件指纹和实际本地Git状态另存本轮交接快照，可读材料同步到CV4独立目录，不覆盖旧交付。

## 当前轮验证

本轮实际重算：51/51静态、14/14交付、18/18生成器输入核查（1个完整输入基准+17个故意损坏反例），两项回归测试通过；历史统计不作为本轮结论。`build_design.py --check` 从输入在内存重建并比较六份生成产物，零写入；异常临时副本测试验证漂移返回1且输入/产物字节保持。

HTML目视日期2026-10-02；Codex In-app Browser，HTTP请求User-Agent报告 Chrome/154.0.0.0；视口1024×768与800×768。实际检查9章目录跳转、标题层级、SVG、P22/P30/P41长表、横向滚动/键盘聚焦、中文显示和本地交接链接（HTTP200，字节相同）。发现名称列过窄、中文逐字换行，已在生成器设置控件表1940px和明确列宽，重建后复查正常；滚动区可Tab聚焦并ArrowRight横移。1024固定目录、800流式目录，主体无整体横向溢出。

字体CSS包含Microsoft YaHei与sans-serif fallback，当前Windows显示正常；无微软雅黑环境与Win7字体实测仍待C。已查看浏览器解析的print CSS（目录隐藏、表宽100%、行断页），未执行实际打印预览分页或实物。页面检查记录和14张检查截图随本地交接包保存，截图含发现问题与修复后的对照；最终 HTML 的 SHA-256 与实际检查记录由发布快照固定。这项目视不代替Win32/Win7/GDI/xlsx验收。

作者检查仅静态设计和HTML文档，不运行实际 Win32、导入事务/幂等、规则引擎、快照锁、GDI/xlsx版式、实物打印或 Win7 VM；无 L1/L2/L3 兼容验收。RV01–RV09 均待非作者 R；没有导入人员原值，不虚报实测人数。

## 待协作与下次起点

A/R：批准候选筛选白名单、搜索语义、状态/死亡日期更正规则、报告接口、Profile唯一匹配、重复候选、枚举/党员代码、PersonCode与工号关系；甲方补样表/模板意向。C：VS2017/v141_xp、Win7 RTM、字体/DPI/设备/硬边距/GDI/xlsx证据。R：发布后固定新#3 HEAD，复核main/base/merge-base、CV4、mapping/FieldChange/D3/YearCount/人数，走RV并提交Formal Review。

提交主题：`docs: 对齐D1B与ContractVersion4并重建复核证据`。用户已明确授权 commit、push、更新 PR 正文与评论；实际提交/发布结果及提交后检查由 PR 和发布快照记录。本轮不新增 PR，不执行合并；PR 保持 Draft，Gate 0 未通过，待非作者 R 对实际审查头进行 Formal Review。
