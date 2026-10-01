#include "retiree_roster/schema_types.hpp"
#include <cassert>
#include <type_traits>
#include <utility>

using namespace retiree_roster::schema;

template <typename T, typename = void>
struct HasStatusResolution : std::false_type {};
template <typename T>
struct HasStatusResolution<T, decltype(void(std::declval<T>().status_resolution))>
    : std::true_type {};

int main() {
    ImportPreview preview;
    preview.batch_id = "batch-example";
    preview.preview_revision = "opaque-checked-revision";
    ConfirmImportRequest confirm;
    confirm.batch_id = preview.batch_id;
    confirm.preview_revision = preview.preview_revision;
    assert(confirm.preview_revision == "opaque-checked-revision");
    static_assert(!HasStatusResolution<ConfirmImportRequest>::value,
                  "confirmation must not resubmit a changed status decision");
}
