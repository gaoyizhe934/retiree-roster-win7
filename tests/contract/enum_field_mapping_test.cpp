#include "retiree_roster/schema_types.hpp"
#include <cassert>
#include <cstdint>
#include <set>

using namespace retiree_roster::schema;

template <typename InputField>
struct MappingCase { InputField input; FieldId expected; };

template <typename InputField, std::size_t N>
void check_mappings(const MappingCase<InputField> (&cases)[N], bool for_import) {
    std::set<FieldId> expected_targets;
    for (const auto& item : cases) {
        FieldId actual = FieldId::PersonId;
        assert(try_to_person_field(item.input, &actual));
        assert(actual == item.expected);
        assert(expected_targets.insert(actual).second);
        const auto* spec = find_person_field(actual);
        assert(spec != nullptr && !spec->system_managed);
        assert(for_import ? spec->source_importable : spec->user_editable);
        assert(!try_to_person_field(item.input, nullptr));
    }
    std::size_t recognized = 0;
    for (unsigned value = 0; value <= 255; ++value) {
        FieldId output = FieldId::PersonId;
        if (try_to_person_field(static_cast<InputField>(value), &output)) {
            assert(expected_targets.count(output) == 1);
            ++recognized;
        } else {
            assert(output == FieldId::PersonId);  // Failed conversion does not overwrite output.
        }
    }
    assert(recognized == N);
    FieldId untouched = FieldId::FullName;
    assert(!try_to_person_field(InputField::Unspecified, &untouched));
    assert(untouched == FieldId::FullName);
}

int main() {
    const MappingCase<ImportFieldId> import_cases[] = {
        {ImportFieldId::EmployeeNo, FieldId::EmployeeNo},
        {ImportFieldId::FullName, FieldId::FullName},
        {ImportFieldId::NationalId, FieldId::NationalId},
        {ImportFieldId::Sex, FieldId::Sex},
        {ImportFieldId::Ethnicity, FieldId::Ethnicity},
        {ImportFieldId::BirthDate, FieldId::BirthDate},
        {ImportFieldId::OriginalOrganization, FieldId::OriginalOrganization},
        {ImportFieldId::Phone, FieldId::Phone},
        {ImportFieldId::HomeAddress, FieldId::HomeAddress},
        {ImportFieldId::RetirementDate, FieldId::RetirementDate},
        {ImportFieldId::PersonnelCategory, FieldId::PersonnelCategory},
        {ImportFieldId::CadreRank, FieldId::CadreRank},
        {ImportFieldId::ProfessionalTitle, FieldId::ProfessionalTitle},
        {ImportFieldId::PositionTitle, FieldId::PositionTitle},
        {ImportFieldId::Education, FieldId::Education},
        {ImportFieldId::Degree, FieldId::Degree},
        {ImportFieldId::WorkStartDate, FieldId::WorkStartDate},
        {ImportFieldId::PartyBranch, FieldId::PartyBranch},
        {ImportFieldId::PartyFullMemberDate, FieldId::PartyFullMemberDate},
        {ImportFieldId::NativePlace, FieldId::NativePlace},
        {ImportFieldId::RelativePhone, FieldId::RelativePhone},
        {ImportFieldId::IdentityCategory, FieldId::IdentityCategory},
        {ImportFieldId::PoliticalAffiliation, FieldId::PoliticalAffiliation},
        {ImportFieldId::PartyJoinDate, FieldId::PartyJoinDate},
        {ImportFieldId::LifeStatus, FieldId::LifeStatus},
        {ImportFieldId::DeathDate, FieldId::DeathDate},
        {ImportFieldId::Remark, FieldId::Remark},
    };
    const MappingCase<EditableFieldId> edit_cases[] = {
        {EditableFieldId::EmployeeNo, FieldId::EmployeeNo},
        {EditableFieldId::FullName, FieldId::FullName},
        {EditableFieldId::PinyinSortKey, FieldId::PinyinSortKey},
        {EditableFieldId::NationalId, FieldId::NationalId},
        {EditableFieldId::Sex, FieldId::Sex},
        {EditableFieldId::Ethnicity, FieldId::Ethnicity},
        {EditableFieldId::BirthDate, FieldId::BirthDate},
        {EditableFieldId::OriginalOrganization, FieldId::OriginalOrganization},
        {EditableFieldId::Phone, FieldId::Phone},
        {EditableFieldId::HomeAddress, FieldId::HomeAddress},
        {EditableFieldId::RetirementDate, FieldId::RetirementDate},
        {EditableFieldId::PersonnelCategory, FieldId::PersonnelCategory},
        {EditableFieldId::CadreRank, FieldId::CadreRank},
        {EditableFieldId::ProfessionalTitle, FieldId::ProfessionalTitle},
        {EditableFieldId::PositionTitle, FieldId::PositionTitle},
        {EditableFieldId::Education, FieldId::Education},
        {EditableFieldId::Degree, FieldId::Degree},
        {EditableFieldId::WorkStartDate, FieldId::WorkStartDate},
        {EditableFieldId::PartyBranch, FieldId::PartyBranch},
        {EditableFieldId::PartyFullMemberDate, FieldId::PartyFullMemberDate},
        {EditableFieldId::NativePlace, FieldId::NativePlace},
        {EditableFieldId::RelativePhone, FieldId::RelativePhone},
        {EditableFieldId::IdentityCategory, FieldId::IdentityCategory},
        {EditableFieldId::PoliticalAffiliation, FieldId::PoliticalAffiliation},
        {EditableFieldId::PartyJoinDate, FieldId::PartyJoinDate},
        {EditableFieldId::LifeStatus, FieldId::LifeStatus},
        {EditableFieldId::DeathDate, FieldId::DeathDate},
        {EditableFieldId::Remark, FieldId::Remark},
    };
    check_mappings(import_cases, true);
    check_mappings(edit_cases, false);
}
