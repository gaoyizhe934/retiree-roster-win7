#include "retiree_roster/schema_types.hpp"
#include <cassert>
#include <type_traits>
#include <utility>

using namespace retiree_roster::schema;

template <typename T, typename = void> struct HasAudit : std::false_type {};
template <typename T> struct HasAudit<T, decltype(void(std::declval<T>().audit))> : std::true_type {};
template <typename T, typename = void> struct HasPersonId : std::false_type {};
template <typename T> struct HasPersonId<T, decltype(void(std::declval<T>().person_id))> : std::true_type {};
template <typename T, typename = void> struct HasUpdatedAt : std::false_type {};
template <typename T> struct HasUpdatedAt<T, decltype(void(std::declval<T>().updated_at))> : std::true_type {};

int main() {
    CreatePersonRequest create;
    create.person.full_name = "Synthetic Person";
    create.person.life_status = LifeStatus::Living;
    static_assert(!HasAudit<decltype(create.person)>::value, "create input cannot supply audit");
    static_assert(!HasPersonId<decltype(create.person)>::value, "create input cannot supply system ID");
    static_assert(!HasUpdatedAt<TagMutation>::value, "tag input cannot supply timestamp");
    static_assert(!std::is_assignable<ImportFieldId&, FieldId>::value, "import targets must exclude system fields");
    static_assert(!std::is_assignable<EditableFieldId&, FieldId>::value, "edit targets must exclude system fields");
    const FieldId protected_fields[] = {FieldId::PersonId, FieldId::PersonCode, FieldId::CreatedAt,
        FieldId::UpdatedAt, FieldId::ImportBatchId, FieldId::LastModifiedBy};
    for (auto field : protected_fields) {
        const auto* spec = find_person_field(field);
        assert(!spec->source_importable && !spec->user_editable && spec->system_managed);
        ImportColumnBinding forged;
        forged.disposition = ImportColumnDisposition::PersonField;
        forged.target_field = static_cast<ImportFieldId>(field);
        assert(!is_valid_import_binding(forged));
        FieldChange edit;
        edit.field = static_cast<EditableFieldId>(field);
        assert(!is_valid_field_change(edit));
    }
    assert(!find_person_field(FieldId::PinyinSortKey)->source_importable);
    assert(find_person_field(FieldId::PinyinSortKey)->user_editable);
    ImportColumnBinding status;
    status.disposition = ImportColumnDisposition::PersonField;
    status.target_field = ImportFieldId::LifeStatus;
    assert(!is_valid_import_binding(status));
    status.status_source_confirmed = true;
    assert(is_valid_import_binding(status));
    FieldChange pinyin;
    pinyin.field = EditableFieldId::PinyinSortKey;
    assert(is_valid_field_change(pinyin));
}
