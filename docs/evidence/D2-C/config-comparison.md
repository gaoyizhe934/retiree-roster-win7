# D2-C 双构建配置对照

- 正式入口：`CMakeLists.txt`（CMake 3.15.7）
- 开发辅助镜像：`xmake.lua`（XMake 2.9.9）
- 工具集选择与镜像口径按 [OD-0003](../../decisions/OD-0003-D2正式构建工具集与镜像口径.md) 执行。
- 同一源目录、同一组业务源、同一组契约头文件与依赖源码；两套不得各自维护另一套业务源。

| 配置项 | CMake（正式） | XMake（辅助） |
| --- | --- | --- |
| 平台 / 架构 | `-G "Visual Studio 15 2017" -A Win32` | `-p windows -a x86` |
| 工具链 | `-T v141_xp` 选择；`project()` 后断言 `CMAKE_VS_PLATFORM_TOOLSET=v141_xp`（MSVC 14.16.27023） | `--toolchain=msvc --vs=2017`（v141 编译器，不启用 v141_xp，见 OD-0003） |
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
  cmake -S . -B build\vs2017-win32-release -G "Visual Studio 15 2017" -A Win32 -T v141_xp -DAPP_STATIC_RUNTIME=ON -DAPP_ENABLE_TESTS=ON
  cmake --build build\vs2017-win32-release --config Release
  cd build\vs2017-win32-release && ctest -C Release --output-on-failure   # CMake 3.15 的 ctest 无 --test-dir
  cmake --install build\vs2017-win32-release --config Release --prefix dist\candidate

XMake:
  xmake f -p windows -a x86 -m release --toolchain=msvc --vs=2017
  xmake build
  xmake run roster_tests
```

## 说明

- 正式工具集只通过命令行 `-T v141_xp` 选择；`CMakeLists.txt` 不修改 `CMAKE_GENERATOR_TOOLSET`（CMake 明确该变量不应由 project code 设置），仅在 `project()` 后断言实际工具集。未带 `-T v141_xp` 的配置会被断言拒绝（见 [cmake-toolset-assertion.txt](cmake-toolset-assertion.txt)）。
- 规划中的固定 CMake 命令补 `-T v141_xp`，其余参数不变；该修订由 [OD-0003](../../decisions/OD-0003-D2正式构建工具集与镜像口径.md) 登记并解决基线命令缺口。
- XMake 的 `--vs=2017` 使用同一 v141 编译器（14.16），不启用 `v141_xp` 平台工具集；按 OD-0003，XMake 仅作开发机镜像，正式候选包只由 CMake install 生成。
- CMake 3.15 的 ctest 尚未提供 `--test-dir`，实际执行等价于在 `build\vs2017-win32-release` 内运行 `ctest -C Release --output-on-failure`。
- `v141_xp` 触发 MSB8051 弃用提示（VS 对 XP 支持的通用提示），不影响构建与运行。
