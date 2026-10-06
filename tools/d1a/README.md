# D1-A 源表盘点与映射覆盖检查

在仓库根目录执行（Python 3 标准库，无第三方依赖、无网络）：

```text
python tools/d1a/inventory_d1a.py
```

生成 L0 证据文件（写入受版本控制的证据目录）：

```text
python tools/d1a/inventory_d1a.py --evidence-dir docs/evidence/D1-A
```

检查器自身的失败路径回归（隔离临时目录，不修改仓库文件）：

```text
python tests/contract/check_d1a_regressions.py --log docs/evidence/D1-A/02-checker-regression.txt
```

刷新受版本控制的 L0 证据（仅在确认差异来自预期改动时使用）：

```text
python tests/contract/check_d1a_regressions.py --log docs/evidence/D1-A/02-checker-regression.txt --update-evidence
```

## 选项

| 选项 | 用途 |
| --- | --- |
| `--root <目录>` | 指定仓库根目录，默认是脚本所在树的根；供隔离回归使用 |
| `--sample <相对路径>` | 覆盖样表路径；指定替代样本时不做基线指纹断言，只记录摘要 |
| `--output <目录>` | results.json 输出目录，默认 `<root>/build/d1a` |
| `--evidence-dir <目录>` | 另写 UTF-8 证据文本（LF 行尾，与宿主控制台代码页无关） |
| `--update-evidence`（回归脚本） | 重新生成两份 L0 证据，而不是校验它们 |

`--sample` 用于回归验证：替代样本不会被基线指纹“挡住”，因此结构检查本身必须失败，否则说明检查是橡皮图章。`--evidence-dir` 与 `--sample` 不能同时使用，受版本控制的证据只能来自已声明样表。

stdout 与 `--evidence-dir` 写出的报告逐字节相同（末尾多一行 `results.json -> …`），因此可以直接用输出比对证据文件是否过期。

## 检查范围

- 公开样表 `reference/员工信息表11111.xlsx` 的 SHA-256 必须等于基线指纹；指纹变化即失败。
- 工作表发现（`xl/workbook.xml` 与关系文件）、共享字符串、合并单元格、含非空单元格的行。
- 表头行号取自 [07_源表字段映射.md](../../docs/baseline/07_源表字段映射.md) 的声明行，不写死在脚本里；声明与工作表不一致即失败。
- 区域 1 逐列：列集合、顺序、规范化键必须与文档表一致；处置必须是 `PersonField`／`BatchRawOnly`／`Unsupported` 之一。
- 区域 2 逐列：沿用 [02_字段映射与数据保留策略.md](../../docs/baseline/02_字段映射与数据保留策略.md) 的候选映射表，同样校验列集合与规范化键。
- 目标合法性：`PersonField` 目标必须是 canonical `PersonFieldId`、必须 `source_importable`、必须存在 `ImportFieldId` 映射；`BatchRawOnly` 与 `Unsupported` 的目标必须是 `-`。
- 唯一目标：同一区域内不得有两个源列映射到同一目标（对应“不允许多源列静默覆盖同一字段”）。
- 状态源：目标为 `LifeStatus` 的行必须在说明中带 `status_source_confirmed` 标记。
- 冲突声明：文档声明的“区域 1 精确重复键”和“跨区域精确同名键”必须与实际计算一致。
- 声明输入：文档声明的样表路径、工作表名与维度必须与实际工作簿一致。
- 跨区域目标一致性：在两区域同名的键，其 canonical 目标必须一致（这是目标“语义”唯一的机器独立校验来源）。
- 漂移保护：工作表出现任何未声明的非空行（数据行或新表头区域）即失败，必须先更新 D1-A 盘点文档。
- 证据新鲜度：回归脚本重新生成盘点报告并与受版本控制的证据逐字节比对；手工改过的证据文件会被判定为过期。
- 合并单元格与受保护区域一并记录，作为表头区域的补充证据。

## 检查边界（工具不做什么）

工具验证的是**合法性、唯一性、跨区域一致性与漂移**，不是处置的语义正确性。区域 1 中有 8 个 `PersonField` 目标（手机、离退休时间、类别、所属支部、原部门、人员状态、转正日期、现学历）在区域 2 没有同名键可比对，机器只能验证其合法与唯一；这类目标选得对不对，属于 R 的逐项人工复核，见 [D1-A 未决项清单](../../docs/baseline/09_D1A未决项清单.md)。

## 失败路径回归（12 项 + 2 项证据校验）

`tests/contract/check_d1a_regressions.py` 在临时目录中复制输入并逐项制造漂移，证明检查器会失败：

| 用例 | 制造的错误 | 期望 |
| --- | --- | --- |
| baseline_tree | 无（基线副本） | 退出 0 |
| undeclared_data_row | 样表插入第 2 行数据 | 未声明的非空行 |
| renamed_header | 样表把“备注”改成“备注X” | 标题规范化键不一致 |
| duplicate_person_target | 两个源列映射到同一目标 | 候选目标重复 |
| batch_raw_only_target | BatchRawOnly 带目标字段 | 必须使用目标 `-` |
| collision_declaration | 少声明一个精确重复键 | 精确重复键声明不一致 |
| status_source_marker | 去掉 `status_source_confirmed` | 缺少状态源标记 |
| unimportable_target | 目标改成不可导入字段 | 目标不可由源表导入 |
| header_row_declaration | 表头行号声明错误 | 声明的表头行不存在 |
| cross_region_target_mismatch | 同名键在两区域映射到不同字段 | 同名键目标不一致 |
| declared_sheet_mismatch | 声明的工作表名错误 | 声明工作表名不一致 |
| declared_sample_mismatch | 声明的样表路径错误 | 声明样表路径与实际输入不一致 |
| committed_inventory_matches | 重新生成盘点报告并与证据比对 | 逐字节一致 |
| committed_regression_log_matches | 本日志与受版本控制证据比对 | 逐字节一致 |

回归日志保存为 [02-checker-regression.txt](../../docs/evidence/D1-A/02-checker-regression.txt)。

## 证据边界

- 脚本只输出表头文本、列身份与计数；**不输出非表头行的单元格值**，因此不会把人员数据写进证据。
- 样表当前没有数据行，报告结论为 `HEADER_ONLY_SAMPLE`；重复率、日期分布、脏数据比例与枚举实际值域一律标记“未测量”。
- 本工具不实现导入、不建数据库、不计算年龄或党龄、不冻结任何业务口径；它不替代 [Gate 0 runner](../gate0/README.md)，也不替代 C 轨的正式 MSVC／Win7 验证。
- 结果 JSON 写入被忽略的 `build/d1a/results.json`，含输入指纹与统计；`--evidence-dir` 另写 UTF-8 文本证据。

## 与 Gate 0 runner 的关系

`tools/gate0/check_contract.py` 目前只校验区域 2 的 23 列映射。把本检查接入 runner 属于跨轨变更，需 R 同意后另行提交，见 [D1-A 未决项清单](../../docs/baseline/09_D1A未决项清单.md) 的 A-D1-15。
