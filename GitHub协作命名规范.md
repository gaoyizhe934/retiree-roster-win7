# GitHub 协作命名规范

本文件补齐仓库原有缺失链接；分支命名依据 [OD-0001 原始指令记录](docs/decisions/OD-0001-分支命名规则.md)。其 ASCII 规则替代旧文档的中文分支示例，仅影响新分支命名。原始 Word/Excel 保留不改。

## 分支

格式为 `类型/简短英文主题`，完整名称仅用 ASCII 字符，满足 `^(feat|fix|docs|test|refactor|chore)/[a-z0-9]+(?:-[a-z0-9]+)*$`。创建前执行 `git check-ref-format --branch <名称>`。禁止 `codex/` 前缀，不擅自重命名已有他人分支或删除远程分支。

示例：`fix/gate0-baseline-stabilization`、`docs/d1b-workflow-template-design`。

## 提交、PR 与任务边界

Commit 和 PR 标题统一为 `类型: 中文变更摘要`；正文和评审报告使用中文。仅允许上述六种类型，一个提交聚焦一个可审查主题。

PR 正文首行标明真实任务编号，如 `阶段/轨道：D1B`。每张任务卡一张 PR；返工留在原 PR，不按自然日拆分，也不把不同轨道或 Gate 混在一起。基线稳定化是 Gate 0 的共同缺口修复，不能虚构为已完成的 A/B/C 任务卡。

技术债先登记文档，再创建同编号 Issue，编号为 `TD-年份-三位流水号`。未获明确授权时只准备待同步材料。

## 发布授权

默认保留未暂存 Diff 供人工审核。commit、push、创建 PR、合并 PR 分别需要用户明确授权。作者不得代签 R 的 Gate 结论；规则全文见 [CONTRIBUTING.md](CONTRIBUTING.md)。
