#include "retiree_roster/schema_types.hpp"
#include <cassert>
#include <set>
#include <type_traits>

using namespace retiree_roster::schema;

int main() {
    PersonRecord person;
    assert(person.life_status == LifeStatus::Unknown);
    assert(FilterSpec{}.life_status == LifeStatusFilter::Unspecified);
    const FieldSpec* status = find_person_field(FieldId::LifeStatus);
    assert(status != nullptr && !status->required_for_import);
    assert(find_person_field(FieldId::RelativePhone)->sensitive);
    assert(!find_person_field(FieldId::PersonId)->printable_by_default);
    assert(!find_person_field(FieldId::PersonCode)->user_editable);
    assert(find_person_field("job_title") == nullptr);
    assert(find_person_field("tag_codes") == nullptr);

    std::set<std::string> keys;
    std::set<FieldId> ids;
    for (const auto& spec : person_field_specs()) {
        assert(keys.insert(spec.key).second);
        assert(ids.insert(spec.id).second);
        assert(find_person_field(spec.key) == &spec);
        assert(find_person_field(spec.id) == &spec);
    }

    // Compile a consumer of the R02 shape, without claiming a rule engine exists.
    FilterSpec chongyang;
    chongyang.target_year = 2026;
    chongyang.as_of_date = {2026, 10, 1, DatePrecision::FullDate};
    chongyang.scenario = RosterScenario::Chongyang;
    chongyang.life_status = LifeStatusFilter::LivingOnly;
    chongyang.age.enabled = true;
    chongyang.age.accepted_values = {70, 75, 80, 85};
    chongyang.age.has_minimum = true;
    chongyang.age.minimum = 90;
    chongyang.tag_match = MatchMode::Any;
    chongyang.tags.push_back({"condolence", "received", 2026});

    PrintTemplate layout;
    TemplateColumn age;
    age.source = TemplateColumnSource::DerivedField;
    age.derived_field = DerivedColumnId::CalendarYearAge;
    layout.columns.push_back(age);
    TemplateColumn signature;
    signature.source = TemplateColumnSource::BlankSignature;
    layout.columns.push_back(signature);

    // All output requests can identify the very same result without a filter.
    ExportRosterRequest export_request;
    PreviewRosterRequest preview_request;
    PrintRosterRequest print_request;
    export_request.snapshot_id = preview_request.snapshot_id = print_request.snapshot_id = "sample";
    PrintModel model;
    using RosterReference = decltype(*model.roster);
    using TemplateReference = decltype(*model.print_template);
    static_assert(std::is_const<typename std::remove_reference<RosterReference>::type>::value,
                  "adapters must consume read-only roster views");
    static_assert(std::is_const<typename std::remove_reference<TemplateReference>::type>::value,
                  "adapters must consume read-only template views");
}
