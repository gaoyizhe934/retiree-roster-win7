# 第三方依赖与许可证台账

日期：2026-10-01；更新：2026-10-06（D2-C 纳入 SQLite）。版本来自需求 v2.0，不在本轮升级。5 个固定版本的源包已归档并记录 SHA-256（见 [third_party/README.md](../../third_party/README.md)）；其中 SQLite 3.45.3 amalgamation 已 vendored 并纳入 D2 正式构建，其余依赖仍未纳入构建，待各自消费任务卡（D3 导入、D5 导出）。以下为上游许可初核，不构成最终许可证签认。

| 固定依赖 | 上游许可与核对来源 | 静态集成／归属 | Notice 与后续核对 | Win7 状态 |
| --- | --- | --- | --- | --- |
| SQLite 3.45.3 | Public domain；[官方声明](https://www.sqlite.org/copyright.html) | amalgamation 源码 vendored 于 `third_party/sqlite`，两套构建静态编译为 `roster_sqlite`（`SQLITE_THREADSAFE=1`、`SQLITE_OMIT_LOAD_EXTENSION=1`）；源包与文件指纹见 [third_party/README.md](../../third_party/README.md) | 分发库源码无强制 notice，构建脚本另查；已记录实际包与文件指纹 | 主机静态编译与冒烟通过（D2-C）；Win7 运行证据随其消费任务卡（D3）补充 |
| xlsxio_read 0.2.35 | MIT；[官方仓库](https://github.com/brechtsanders/xlsxio)、[许可](https://raw.githubusercontent.com/brechtsanders/xlsxio/master/LICENSE.txt) | 静态 read 库；未引入 | 保留版权和许可；当前分支许可已核，0.2.35 源包原文待归档 | 未验证 |
| Expat 2.2.10 | MIT；[固定 tag COPYING](https://raw.githubusercontent.com/libexpat/libexpat/R_2_2_10/expat/COPYING) | 静态 XML 解析；未引入 | 保留版权和许可；实际源包与 tag 对账 | 未验证 |
| zlib 1.2.13 | zlib；[固定 tag LICENSE](https://github.com/madler/zlib/blob/v1.2.13/LICENSE) | 静态压缩库；未引入 | 源分发保留 notice、改动明确标记；二进制致谢非强制，交付仍归档原许可 | 未验证 |
| libxlsxwriter 1.1.5 | BSD-2-Clause／FreeBSD；[官方许可说明](https://libxlsxwriter.github.io/license.html) | 静态导出库；未引入 | 源与二进制分发保留版权、条款、免责声明；1.1.5 固定源包原文待归档 | 未验证 |

## 传递与附带组件

[xlsxio 官方依赖说明](https://github.com/brechtsanders/xlsxio)要求 Expat 及 minizip 或 libzip，后者依赖 zlib。只写 zlib 不足以说明 ZIP 读取链接方案；C 应确认固定源码包的 minizip 实现／版本／许可与静态链接方式，不能引入额外 DLL。

[libxlsxwriter 官方许可说明](https://libxlsxwriter.github.io/license.html)还列出 queue.h、tree.h、minizip、tmpfileplus（MPL-2.0）、MD5 和可选 dtoa 的独立许可。实际 1.1.5 源包采用哪些代码、各原始 notice、是否启用 tmpfileplus、需要哪些源码提供义务，均待固定包及构建选项核对。不得仅凭主库 BSD 标签宣称整包已完成许可证审核。

## Gate 前待补

- 源包地址与 SHA-256 已记录（[third_party/README.md](../../third_party/README.md)）；各固定版本的原始许可／版权文本仍待随源包归档。
- 源码／二进制归属、修改记录、全部传递组件、静态构建选项及 notice 汇编：SQLite 已随 D2-C 纳入并记录；其余依赖待各自消费任务卡。
- VS2017 v141_xp／Win32／MT 构建与 dumpbin 已随 D2-C 提供（`docs/evidence/D2-C/`）；SQLite 的 Win7 运行证据与双 VM 完整链路随 D3 及后续 Gate。
- 非作者 R 的许可证质量签认及 Gate 链接；创建者的发布授权另行记录。

仓库自身 LICENSE 仍待创建者选择，本轮不添加或推定项目许可证。第三方许可不等于本项目许可。
