-- Auxiliary development mirror of the formal CMake pipeline (D2-C).
-- It must share the same source tree, C++14, Win32, /MT, Unicode,
-- WINVER/_WIN32_WINNT=0x0601 and the same third-party dependencies.
-- The candidate package is produced only by the CMake install step.
--
-- Reproducible commands (recorded in the D2-C evidence):
--   xmake f -p windows -a x86 -m release --toolchain=msvc --vs=2017
--   xmake build
--   xmake run roster_tests

set_project("retiree_roster")
set_version("0.1.0")
set_xmakever("2.9.0")

set_languages("c++14")
set_encodings("utf-8")
set_warnings("all")
set_runtimes("MT")

add_defines("UNICODE", "_UNICODE", "WINVER=0x0601", "_WIN32_WINNT=0x0601")

target("roster_app")
    set_kind("binary")
    set_basename("app")
    add_files("src/ui/main_win32.cpp")
    add_includedirs("include")
    add_syslinks("user32", "gdi32")
    add_ldflags("/SUBSYSTEM:WINDOWS", "/ENTRY:wWinMainCRTStartup", {force = true})

target("roster_sqlite")
    set_kind("static")
    add_files("third_party/sqlite/sqlite3.c")
    add_includedirs("third_party/sqlite", {public = true})
    add_defines("SQLITE_THREADSAFE=1", "SQLITE_OMIT_LOAD_EXTENSION=1")
    set_warnings("none")

local test_sources = {
    "tests/build_config_test.cpp",
    "tests/contract/consumer_contract_test.cpp",
    "tests/contract/date_value_test.cpp",
    "tests/contract/enum_field_mapping_test.cpp",
    "tests/contract/field_change_test.cpp",
    "tests/contract/filter_shape_test.cpp",
    "tests/contract/input_authority_test.cpp",
    "tests/contract/preview_revision_test.cpp",
}

local test_targets = {}
for _, source in ipairs(test_sources) do
    local name = path.basename(source)
    target(name)
        set_kind("binary")
        add_files(source)
        add_includedirs("include")
    table.insert(test_targets, name)
end

target("sqlite_smoke_test")
    set_kind("binary")
    add_files("tests/sqlite_smoke_test.cpp")
    add_deps("roster_sqlite")
table.insert(test_targets, "sqlite_smoke_test")

target("roster_tests")
    set_kind("phony")
    add_deps(table.unpack(test_targets))
    on_run(function (target)
        for _, dep in ipairs(target:orderdeps()) do
            if dep:kind() == "binary" then
                local result = os.execv(dep:targetfile())
                if result == false or (type(result) == "number" and result ~= 0) then
                    raise("test failed: " .. dep:name())
                end
            end
        end
    end)
