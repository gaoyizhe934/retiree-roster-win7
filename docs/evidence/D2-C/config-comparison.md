# D2-C 双构建配置对照

- 正式入口：`CMakeLists.txt`（CMake 3.15.7）
- 开发辅助镜像：`xmake.lua`（XMake 2.9.9）
- 同一源目录、同一组业务源、同一组契约头文件与依赖源码；两套不得各自维护另一套业务源。

| 配置项 | CMake（正式） | XMake（辅助） |
| --- | --- | --- |
| 平台 / 架构 | `-G "Visual Studio 15 2017" -A Win32` | `-p windows -a x86` |
| 工具链 | `CMAKE_GENERATOR_TOOLSET=v141_xp`（MSVC 14.16.27023） | `--toolchain=msvc --vs=2017`（MSVC 14.16.27054） |
| C++ 标准 | `CMAKE_CXX_STANDARD 14`（/std:c++14） | `set_languages("c++14")` |
| 静态运行库 | `CMAKE_MSVC_RUNTIME_LIBRARY=MultiThreaded`（/MT） | `set_runtimes("MT")` |
| Unicode | `add_compile_definitions(UNICODE _UNICODE)` | `add_defines("UNICODE", "_UNICODE")` |
| 目标 OS API | `WINVER=0x0601`、`_WIN32_WINNT=0x0601` | 同左 |
| 源码编码 | `/utf-8` | `set_encodings("utf-8")` |
| 应用目标 | `roster_app`（WIN32 子系统，输出 `app.exe`） | `roster_app`（`set_basename("app")`） |
| 静态依赖 | `roster_sqlite`（`third_party/sqlite/sqlite3.c`，`SQLITE_THREADSAFE=1`、`SQLITE_OMIT_LOAD_EXTENSION=1`） | `roster_sqlite`（同源码、同宏） |
| 测试 | `enable_testing()` + 9 个 `add_test`；`roster_tests` 自定义目标调用 ctest | 9 个测试目标；`roster_tests` 聚合目标依次执行 |
| 候选包 | `cmake --install ... --prefix dist\candidate`（唯一候选包来源） | 不产出候选包（仅本地检查） |

## 与规划命令的对应

```text
CMake:
  cmake -S . -B build\vs2017-win32-release -G "Visual Studio 15 2017" -A Win32 -DAPP_STATIC_RUNTIME=ON -DAPP_ENABLE_TESTS=ON
  cmake --build build\vs2017-win32-release --config Release
  ctest --test-dir build\vs2017-win32-release -C Release --output-on-failure   # 本机 CMake 3.15 无 --test-dir，改为在构建目录内执行 ctest
  cmake --install build\vs2017-win32-release --config Release --prefix dist\candidate

XMake:
  xmake f -p windows -a x86 -m release --toolchain=msvc --vs=2017
  xmake build
  xmake run roster_tests
```

## 说明

- XMake 的 `--vs=2017` 使用同一 v141 编译器（14.16），但不启用 `v141_xp` 平台工具集；`v141_xp` 是 CMake 正式候选包的锁定要求，XMake 仅作开发机配置一致性复核。
- CMake 3.15 的 ctest 尚未提供 `--test-dir`，实际执行等价于在 `build\vs2017-win32-release` 内运行 `ctest -C Release --output-on-failure`。
- `v141_xp` 触发 MSB8051 弃用提示（VS 对 XP 支持的通用提示），不影响构建与运行。
