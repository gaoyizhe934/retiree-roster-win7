# Formal build and release entry (D2-C).
# Locked target: Visual Studio 15 2017 / v141_xp, Win32 (x86), C++14, Unicode,
# static runtime (/MT), WINVER/_WIN32_WINNT=0x0601, Windows 7 SP1.
#
# Reproducible command (recorded in the D2-C evidence):
#   cmake -S . -B build\vs2017-win32-release -G "Visual Studio 15 2017" -A Win32 \
#         -DAPP_STATIC_RUNTIME=ON -DAPP_ENABLE_TESTS=ON
#   cmake --build build\vs2017-win32-release --config Release
#   ctest --test-dir build\vs2017-win32-release -C Release --output-on-failure
#   cmake --install build\vs2017-win32-release --config Release --prefix dist\candidate

cmake_minimum_required(VERSION 3.15)

# CMP0091: select the MSVC runtime through CMAKE_MSVC_RUNTIME_LIBRARY.
cmake_policy(SET CMP0091 NEW)

# The formal toolchain is the VS2017 Windows XP platform toolset.
# Must be a cache entry set before the first project() call.
set(CMAKE_GENERATOR_TOOLSET "v141_xp" CACHE STRING "MSVC platform toolset (formal build)" FORCE)

project(retiree_roster VERSION 0.1.0 LANGUAGES C CXX)

if(NOT MSVC)
    message(FATAL_ERROR "The formal build requires MSVC (Visual Studio 15 2017, v141_xp).")
endif()
if(NOT CMAKE_SIZEOF_VOID_P EQUAL 4)
    message(FATAL_ERROR "The formal distribution is Win32/x86 only; pass -A Win32.")
endif()

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

option(APP_STATIC_RUNTIME "Link the static MSVC runtime (/MT)" ON)
option(APP_ENABLE_TESTS "Build the L1 test suite" ON)

if(APP_STATIC_RUNTIME)
    set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")
else()
    set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>DLL")
endif()

add_compile_definitions(UNICODE _UNICODE WINVER=0x0601 _WIN32_WINNT=0x0601)
add_compile_options(/utf-8)

# --- application (empty window for the D2-C candidate) -------------------
add_executable(roster_app WIN32 src/ui/main_win32.cpp)
set_target_properties(roster_app PROPERTIES OUTPUT_NAME app)
target_include_directories(roster_app PRIVATE include)

# --- third-party static dependencies -------------------------------------
# SQLite amalgamation is vendored in third_party/sqlite (public domain).
add_library(roster_sqlite STATIC third_party/sqlite/sqlite3.c)
target_include_directories(roster_sqlite PUBLIC third_party/sqlite)
target_compile_definitions(roster_sqlite PRIVATE
    SQLITE_THREADSAFE=1
    SQLITE_OMIT_LOAD_EXTENSION=1)
target_compile_options(roster_sqlite PRIVATE /W0)

# --- L1 tests ------------------------------------------------------------
if(APP_ENABLE_TESTS)
    enable_testing()

    set(ROSTER_TEST_SOURCES
        tests/build_config_test.cpp
        tests/contract/consumer_contract_test.cpp
        tests/contract/date_value_test.cpp
        tests/contract/enum_field_mapping_test.cpp
        tests/contract/field_change_test.cpp
        tests/contract/filter_shape_test.cpp
        tests/contract/input_authority_test.cpp
        tests/contract/preview_revision_test.cpp
    )

    set(ROSTER_TEST_TARGETS)
    foreach(source IN LISTS ROSTER_TEST_SOURCES)
        get_filename_component(name "${source}" NAME_WE)
        add_executable(${name} "${source}")
        target_include_directories(${name} PRIVATE include)
        add_test(NAME ${name} COMMAND ${name})
        list(APPEND ROSTER_TEST_TARGETS ${name})
    endforeach()

    add_executable(sqlite_smoke_test tests/sqlite_smoke_test.cpp)
    target_link_libraries(sqlite_smoke_test PRIVATE roster_sqlite)
    add_test(NAME sqlite_smoke_test COMMAND sqlite_smoke_test)
    list(APPEND ROSTER_TEST_TARGETS sqlite_smoke_test)

    add_custom_target(roster_tests
        COMMAND ${CMAKE_CTEST_COMMAND} --output-on-failure -C $<CONFIG>
        WORKING_DIRECTORY "${CMAKE_BINARY_DIR}"
        DEPENDS ${ROSTER_TEST_TARGETS}
        COMMENT "Running the L1 test suite"
        USES_TERMINAL)
endif()

# --- packaging: the candidate package only comes from CMake install ------
install(TARGETS roster_app RUNTIME DESTINATION .)
install(DIRECTORY packaging/package/ DESTINATION .
        PATTERN ".gitkeep" EXCLUDE)
