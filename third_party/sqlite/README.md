# SQLite amalgamation（vendored）

- 版本：3.45.3
- 源包：https://www.sqlite.org/2024/sqlite-amalgamation-3450300.zip
- 源包 SHA-256：`EA170E73E447703E8359308CA2E4366A3AE0C4304A8665896F068C736781C651`
- 文件指纹：
  - `sqlite3.c`：`9CA336FBCBFF9F1D78B4F45B6A19583FCC097192310DD2F5F6CD43B9A33D7D69`
  - `sqlite3.h`：`882AD3C0448D0324FB3A6B1A85333A9173D539AC669C9972AE1F03722FF86282`
  - `sqlite3ext.h`：`B184DD1586D935133D37AD76FA353FAF0A1021FF2FDEDEEDCC3498FFF74BBB94`
- 许可：Public domain（https://www.sqlite.org/copyright.html），分发无强制 notice。
- 构建：`sqlite3.c` 不经修改，由 CMake 与 XMake 分别静态编译为 `roster_sqlite`；仅从 amalgamation 随附文件中引入 `sqlite3.c`、`sqlite3.h`、`sqlite3ext.h`（未使用 `shell.c`）。
