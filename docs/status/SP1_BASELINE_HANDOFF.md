# Windows 7 SP1 基线修订与跨轨交接

日期：2026-10-03。当前 main 起点为 `567d9cd32befc2b8aa7ae99487f8b6d2170f1436`。本分支只承载 [OD-0002](../decisions/OD-0002-Windows7-SP1目标基线.md)、三份受控文件修订、指纹及当前入口/状态统一；新基线尚未合入 main。

## 当前 PR 与依赖顺序

| 轨道 | 唯一有效 PR / 已核对 head | 本次后续操作 | 尚未完成的条件 |
| --- | --- | --- | --- |
| A | [#6](https://github.com/gaoyizhe934/retiree-roster-win7/pull/6) / 32433bcc815c8eded10aab69bccf9c771abc7d94 | 按 Q1-B/Q2-A 同步 06/07/09/Review Packet；重跑 A L0 与回归 | 新 HEAD 的 R 复核；五个 Unsupported 和八个语义项继续 D3 |
| B | [#3](https://github.com/gaoyizhe934/retiree-roster-win7/pull/3) / 2f9de31b81bf788da9c06f69946b501c29b394e0 | 基线进入 main 后更新设计正文的当前 RTM 条款、交付记录，重新生成 MD/HTML/JSON | build_design.py --check、test_build_design.py、新 HEAD Formal Review |
| C | [#7](https://github.com/gaoyizhe934/retiree-roster-win7/pull/7) / fba99e0d2569faabb24a26b9d025951a6e20b4f1 | 基线进入 main 后在 VM 完成说明及接手记录引用 OD-0002 | 新增 Guest 截图待 R 复核；缺失来源/错误链接、正式工具链证据 |

新全局基线 PR 不吸收阶段交付文件、不重建 #3/#6/#7、不改他们的现有 Review 结论。A 的 Q1/Q2 修改在 #6 继续；B/C 的当前声明等新基线进入 main 后沿原 PR 落地。上述阶段尚未同步，不能将计划记成已完成。

所有分支整合通过 GitHub PR；每次合并都须用户明确授权及必要评审。不能本地 merge/rebase；同步已合并的线性内容仅使用 `git pull --ff-only`。若现有阶段分支不能快进，保留现场，通过 GitHub PR 安排 main 到该阶段分支的基线整合，而不强推或重建阶段 PR。集成 PR 只运送基线，不替代阶段成果 PR。

## 已取得的 A 人类决定

来源为本任务 2026-10-03 的直接回答：

> Q1-B：确认首期只有这一份
>
> Q2-A：两套都作为首期 Source Profile（清单建议）

Q1 是首期业务范围确认，不声称世界上不存在其他文件，也不推导 Q2。Q2 分别使用 P1（Sheet1 行1、52 标题）与 P2（行3、23 标题）；保留物理区域及全部列处置，0 数据行事实不变。五个 Unsupported 和八个机器不能核验的映射语义留 D3；Profile 地位确认不等于映射、值域和导入策略已批准。

A 的 06/07/09/Review Packet 必须一致：NO_SECOND_BUSINESS_WORKBOOK、BOTH_SOURCE_PROFILES，未回答人类决定为 0。复跑：

```text
python tools/d1a/inventory_d1a.py --evidence-dir docs/evidence/D1-A
python tests/contract/check_d1a_regressions.py --log docs/evidence/D1-A/02-checker-regression.txt
```

新基线改了任务台账指纹，A/B 检查器若另有硬编码或生成输入指纹，须按其单一来源同步；业务样表指纹保持不变，不复制旧证据。A/B 文件目前仅在各自未合并 PR，不在 main。

## C 证据边界

VM 名称 Win7RTM-SP1-x86/x64 是当前机器的历史命名，不手改 VBoxManage 原始输出。OD-0002 只关闭目标 OS 的条款冲突；说明应写“目标基线已决定，阶段证据仍待复核”。C #7 在 fba99e0 已新增 x86/x64 的 winver、appwiz.cpl 与 systeminfo 截图；本次只核对文件增量，尚未完成图像审查，也未取得该新 HEAD 的 R 复核。Guest 版本及纯净性须由真实证据和正式复核确认，不能用说明文字替代。缺失交接源文件与错误链接单独修复并由 R 检查。

## 本分支验证及发布

```text
python tools/gate0/check_contract.py --layer structure --base-ref origin/main
python tools/gate0/check_contract.py --layer cpp14 --base-ref origin/main
python tools/gate0/check_contract.py --layer diff --base-ref origin/main
python tools/gate0/check_contract.py --layer all --base-ref origin/main
```

本地 JSON、OOXML 对照与渲染 QA 放在忽略目录 build/gate0/sp1。未提交候选由输入指纹标识；commit/push 后在实际 head 复跑，真实 SHA 和数字写入 PR 正文，tracked 文档不追写自己的 SHA。作者检查不代替 Formal Review，不证明 Win7 L2/L3 或 Gate 0 PASS。
