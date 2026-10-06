# 第三方依赖归档与构建边界

本目录是固定第三方依赖的**唯一构建来源**。版本、上游地址与 SHA-256 是身份依据；不得用同名不同内容的文件替换。

## 源包归档

原始源包保存在本地（由 `.gitignore` 排除，不入库），SHA-256 用于独立复核：

| 依赖 | 版本 | 上游源包 | SHA-256 |
| --- | --- | --- | --- |
| SQLite | 3.45.3 | https://www.sqlite.org/2024/sqlite-amalgamation-3450300.zip | `EA170E73E447703E8359308CA2E4366A3AE0C4304A8665896F068C736781C651` |
| xlsxio_read | 0.2.35 | https://github.com/brechtsanders/xlsxio/archive/refs/tags/0.2.35.zip | `8AEB666BA7039E550E067EBE7B522D1ED8C16456C05740B647F449FB2EBC082C` |
| Expat | 2.2.10 | https://github.com/libexpat/libexpat/releases/download/R_2_2_10/expat-2.2.10.tar.gz | `BF42D1F52371D23684DE36CC6D2F0F1ACD02DE264D1105BDC17792BBEB7E7CEB` |
| zlib | 1.2.13 | https://github.com/madler/zlib/archive/refs/tags/v1.2.13.zip | `C2856951BBF30E30861ACE3765595D86BA13F2CF01279D901F6C62258C57F4FF` |
| libxlsxwriter | 1.1.5 | https://github.com/jmcnamara/libxlsxwriter/archive/refs/tags/RELEASE_1.1.5.zip | `8441C6599FD45BE84BC1A39DE0DEC670176D5B0F237F54D14DDAF170EDBC5D65` |

本地归档目录：`third_party/archives/`（不入库）。

## 已纳入构建的源码

| 目录 | 内容 | 许可 | 说明 |
| --- | --- | --- | --- |
| `third_party/sqlite/` | SQLite 3.45.3 amalgamation（`sqlite3.c`/`sqlite3.h`/`sqlite3ext.h`） | Public domain | D2-C 起由 CMake 与 XMake 静态编译为 `roster_sqlite` |

xlsxio_read、Expat、zlib、libxlsxwriter 在各自被消费的任务卡（D3 导入、D5 导出）纳入构建；纳入时两套构建文件必须使用同一份源码与同一组宏。

## 许可与 notice

许可初核见 [docs/dependencies/THIRD_PARTY.md](../docs/dependencies/THIRD_PARTY.md)。传递组件（minizip、tmpfileplus 等）随对应源包纳入时再行核对。
