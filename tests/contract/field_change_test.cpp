#include "retiree_roster/schema_types.hpp"
#include <cassert>

using namespace retiree_roster::schema;

int main() {
    const EditableFieldId dates[] = {EditableFieldId::BirthDate, EditableFieldId::RetirementDate,
        EditableFieldId::WorkStartDate, EditableFieldId::PartyFullMemberDate,
        EditableFieldId::PartyJoinDate, EditableFieldId::DeathDate};
    for (auto field : dates) {
        FieldChange change;
        change.field = field;
        change.date_value = {1956, 0, 0, DatePrecision::Year};
        assert(is_valid_field_change(change));
        change.date_value = {1956, 10, 0, DatePrecision::YearMonth};
        assert(is_valid_field_change(change));
        change.date_value = {1956, 10, 2, DatePrecision::FullDate};
        assert(is_valid_field_change(change));
        change.value = "1956-10-02";
        assert(!is_valid_field_change(change));  // Date payload must not also carry text.
        change.date_value = {};
        assert(!is_valid_field_change(change));  // Text never implicitly parses to a date.
        change.value.clear();
        assert(!is_valid_field_change(change));  // Unknown date is not a date assignment.
        change.date_value = {1956, 2, 30, DatePrecision::FullDate};
        assert(!is_valid_field_change(change));
        change.date_value = {};
        change.clear_value = true;
        assert(is_valid_field_change(change));
        change.value = "unexpected";
        assert(!is_valid_field_change(change));
        change.value.clear();
        change.date_value = {1956, 0, 0, DatePrecision::Year};
        assert(!is_valid_field_change(change));
    }

    FieldChange text;
    text.field = EditableFieldId::FullName;
    text.value = "Synthetic Name";
    assert(is_valid_field_change(text));
    text.date_value = {1956, 0, 0, DatePrecision::Year};
    assert(!is_valid_field_change(text));
    text.date_value = {1956, 0, 0, DatePrecision::Unknown};
    assert(!is_valid_field_change(text));  // Unknown must have canonical zero components.
    text.date_value = {};
    text.clear_value = true;
    assert(!is_valid_field_change(text));
    text.value.clear();
    assert(is_valid_field_change(text));

    FieldChange code;
    code.field = EditableFieldId::LifeStatus;
    code.value = "Living";
    assert(is_valid_field_change(code));
    code.date_value = {1956, 0, 0, DatePrecision::Year};
    assert(!is_valid_field_change(code));
    code.date_value = {};
    code.clear_value = true;
    assert(!is_valid_field_change(code));
    code.value.clear();
    assert(is_valid_field_change(code));  // Required fields and code vocabularies are D3 validation.

    FieldChange forged;
    forged.field = EditableFieldId::Unspecified;
    forged.clear_value = true;
    assert(!is_valid_field_change(forged));
    forged.field = static_cast<EditableFieldId>(254);
    assert(!is_valid_field_change(forged));
}
