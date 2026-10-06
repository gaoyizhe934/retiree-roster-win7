// D2-C: proves the vendored SQLite 3.45.3 amalgamation is linked statically
// in both build pipelines (CMake candidate and XMake development mirror).
#include <cstdio>
#include <cstring>

#include "sqlite3.h"

namespace {

int fail(const char* what) {
    std::fprintf(stderr, "sqlite_smoke_test: FAIL: %s\n", what);
    return 1;
}

}  // namespace

int main() {
    if (std::strcmp(sqlite3_libversion(), "3.45.3") != 0) {
        return fail("unexpected sqlite version");
    }

    sqlite3* database = nullptr;
    if (sqlite3_open(":memory:", &database) != SQLITE_OK) {
        return fail("open :memory:");
    }

    sqlite3_stmt* statement = nullptr;
    if (sqlite3_prepare_v2(database, "SELECT 40 + 2", -1, &statement, nullptr) != SQLITE_OK) {
        sqlite3_close(database);
        return fail("prepare");
    }

    int value = -1;
    if (sqlite3_step(statement) == SQLITE_ROW) {
        value = sqlite3_column_int(statement, 0);
    } else {
        sqlite3_finalize(statement);
        sqlite3_close(database);
        return fail("step");
    }

    sqlite3_finalize(statement);
    sqlite3_close(database);

    if (value != 42) {
        return fail("arithmetic");
    }
    std::puts("sqlite_smoke_test: PASS (SQLite 3.45.3 static)");
    return 0;
}
