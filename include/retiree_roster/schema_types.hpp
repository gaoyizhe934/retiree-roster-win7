#pragma once

#include <array>
#include <cstddef>
#include <cstdint>
#include <memory>
#include <string>
#include <utility>
#include <vector>

// Draft contract: authority and approval live in docs/baseline and Gate Status.
// This header does not define or override business requirements.
// It deliberately uses only C++14 standard-library types for the Win7 target.
namespace retiree_roster {
namespace schema {

using ContractVersion = std::uint32_t;
using DatabaseSchemaVersion = std::uint32_t;  // Independent migration version; not assigned here.
constexpr ContractVersion kCurrentContractVersion = 4U;  // Draft revision, not a Gate freeze.

using PersonId = std::string;
using ImportBatchId = std::string;
using PreviewRevision = std::string;  // Opaque identity of a service-owned, checked preview.
using TemplateId = std::string;
using FilterId = std::string;
using RequestId = std::string;
using UserId = std::string;
using PersonCode = std::string;
using SnapshotId = std::string;
using ExportId = std::string;
using TagCode = std::string;
using DataVersion = std::uint64_t;

// Attribution only. No authentication or authorization is implied.
struct OperatorContext {
    UserId operator_id;
    std::string display_name;
};

enum class DatePrecision : std::uint8_t { Unknown, Year, YearMonth, FullDate };

// Preserve source precision. Missing components are zero, never invented.
struct DateValue {
    std::int32_t year = 0;
    std::uint8_t month = 0;
    std::uint8_t day = 0;
    DatePrecision precision = DatePrecision::Unknown;

    bool is_valid() const {
        if (precision == DatePrecision::Unknown) {
            return year == 0 && month == 0 && day == 0;
        }
        if (year < 1 || year > 9999) { return false; }
        if (precision == DatePrecision::Year) { return month == 0 && day == 0; }
        if (month < 1 || month > 12) { return false; }
        if (precision == DatePrecision::YearMonth) { return day == 0; }
        if (precision != DatePrecision::FullDate) { return false; }
        const std::uint8_t days[] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
        const bool leap = year % 4 == 0 && (year % 100 != 0 || year % 400 == 0);
        const std::uint8_t limit = (month == 2 && leap) ? 29 : days[month - 1];
        return day >= 1 && day <= limit;
    }

    bool is_known() const {
        return precision != DatePrecision::Unknown && is_valid();
    }

    bool is_full_date() const { return precision == DatePrecision::FullDate && is_valid(); }
};

using LocalDate = DateValue;  // Transitional name; precision remains mandatory.

// ISO-8601 UTC text, for example "2026-09-21T08:30:00Z".
// A string is intentional: C++14 has no standard time-zone type.
using UtcTimestamp = std::string;

enum class LifeStatus : std::uint8_t {
    Unknown,  // Must be resolved before create/import confirmation.
    Living,
    Deceased,
};

enum class FieldValueKind : std::uint8_t {
    Text,
    Date,
    EnumCode,
    Identifier,
    Timestamp,
};

// FieldId is the canonical API/database/template identity. Do not pass free-form
// field keys between modules; map source headings to this enum during import.
enum class PersonFieldId : std::uint8_t {
    PersonId,
    PersonCode,
    EmployeeNo,
    FullName,
    PinyinSortKey,
    NationalId,
    Sex,
    Ethnicity,
    BirthDate,
    OriginalOrganization,
    Phone,
    HomeAddress,
    RetirementDate,
    PersonnelCategory,
    CadreRank,
    ProfessionalTitle,
    PositionTitle,
    Education,
    Degree,
    WorkStartDate,
    PartyBranch,
    PartyFullMemberDate,
    NativePlace,
    RelativePhone,
    IdentityCategory,
    PoliticalAffiliation,
    PartyJoinDate,
    LifeStatus,
    DeathDate,
    Remark,
    CreatedAt,
    UpdatedAt,
    ImportBatchId,
    LastModifiedBy,
};
using FieldId = PersonFieldId;  // Person fields only; tags and derived columns are separate.

struct FieldSpec {
    FieldId id;
    const char* key;
    FieldValueKind value_kind;
    bool required_for_import;
    bool sensitive;
    bool source_importable;
    bool user_editable;
    bool system_managed;
    bool printable_by_default;
};

inline const std::array<FieldSpec, 34>& person_field_specs() {
    static const std::array<FieldSpec, 34> kSpecs = {{
        {FieldId::PersonId, "person_id", FieldValueKind::Identifier, false, false, false, false, true, false},
        {FieldId::PersonCode, "person_code", FieldValueKind::Identifier, false, false, false, false, true, true},
        {FieldId::EmployeeNo, "employee_no", FieldValueKind::Text, false, false, true, true, false, true},
        {FieldId::FullName, "full_name", FieldValueKind::Text, true, false, true, true, false, true},
        {FieldId::PinyinSortKey, "pinyin_sort_key", FieldValueKind::Text, false, false, false, true, false, false},
        {FieldId::NationalId, "national_id", FieldValueKind::Text, false, true, true, true, false, false},
        {FieldId::Sex, "sex", FieldValueKind::EnumCode, false, false, true, true, false, true},
        {FieldId::Ethnicity, "ethnicity", FieldValueKind::Text, false, false, true, true, false, true},
        {FieldId::BirthDate, "birth_date", FieldValueKind::Date, false, false, true, true, false, true},
        {FieldId::OriginalOrganization, "original_organization", FieldValueKind::Text, false, false, true, true, false, true},
        {FieldId::Phone, "phone", FieldValueKind::Text, false, true, true, true, false, false},
        {FieldId::HomeAddress, "home_address", FieldValueKind::Text, false, true, true, true, false, false},
        {FieldId::RetirementDate, "retirement_date", FieldValueKind::Date, false, false, true, true, false, true},
        {FieldId::PersonnelCategory, "personnel_category", FieldValueKind::EnumCode, false, false, true, true, false, true},
        {FieldId::CadreRank, "cadre_rank", FieldValueKind::EnumCode, false, false, true, true, false, true},
        {FieldId::ProfessionalTitle, "professional_title", FieldValueKind::Text, false, false, true, true, false, true},
        {FieldId::PositionTitle, "position_title", FieldValueKind::Text, false, false, true, true, false, true},
        {FieldId::Education, "education", FieldValueKind::Text, false, false, true, true, false, true},
        {FieldId::Degree, "degree", FieldValueKind::Text, false, false, true, true, false, true},
        {FieldId::WorkStartDate, "work_start_date", FieldValueKind::Date, false, false, true, true, false, true},
        {FieldId::PartyBranch, "party_branch", FieldValueKind::Text, false, false, true, true, false, true},
        {FieldId::PartyFullMemberDate, "party_full_member_date", FieldValueKind::Date, false, false, true, true, false, true},
        {FieldId::NativePlace, "native_place", FieldValueKind::Text, false, false, true, true, false, true},
        {FieldId::RelativePhone, "relative_phone", FieldValueKind::Text, false, true, true, true, false, false},
        {FieldId::IdentityCategory, "identity_category", FieldValueKind::Text, false, false, true, true, false, true},
        {FieldId::PoliticalAffiliation, "political_affiliation", FieldValueKind::EnumCode, false, false, true, true, false, true},
        {FieldId::PartyJoinDate, "party_join_date", FieldValueKind::Date, false, false, true, true, false, true},
        {FieldId::LifeStatus, "life_status", FieldValueKind::EnumCode, false, false, true, true, false, true},
        {FieldId::DeathDate, "death_date", FieldValueKind::Date, false, false, true, true, false, false},
        {FieldId::Remark, "remark", FieldValueKind::Text, false, false, true, true, false, false},
        {FieldId::CreatedAt, "created_at", FieldValueKind::Timestamp, false, false, false, false, true, false},
        {FieldId::UpdatedAt, "updated_at", FieldValueKind::Timestamp, false, false, false, false, true, false},
        {FieldId::ImportBatchId, "import_batch_id", FieldValueKind::Identifier, false, false, false, false, true, false},
        {FieldId::LastModifiedBy, "last_modified_by", FieldValueKind::Identifier, false, false, false, false, true, false},
    }};
    return kSpecs;
}

inline const FieldSpec* find_person_field(const std::string& key) {
    const auto& specs = person_field_specs();
    for (std::size_t i = 0; i < specs.size(); ++i) {
        if (key == specs[i].key) {
            return &specs[i];
        }
    }
    return nullptr;
}

inline const FieldSpec* find_person_field(FieldId id) {
    const auto& specs = person_field_specs();
    for (std::size_t i = 0; i < specs.size(); ++i) {
        if (id == specs[i].id) {
            return &specs[i];
        }
    }
    return nullptr;
}

inline bool is_current_contract(ContractVersion version) {
    return version == kCurrentContractVersion;
}

enum class ImportFieldId : std::uint8_t {
    Unspecified = 255,
    EmployeeNo = 64,
    FullName,
    NationalId,
    Sex,
    Ethnicity,
    BirthDate,
    OriginalOrganization,
    Phone,
    HomeAddress,
    RetirementDate,
    PersonnelCategory,
    CadreRank,
    ProfessionalTitle,
    PositionTitle,
    Education,
    Degree,
    WorkStartDate,
    PartyBranch,
    PartyFullMemberDate,
    NativePlace,
    RelativePhone,
    IdentityCategory,
    PoliticalAffiliation,
    PartyJoinDate,
    LifeStatus,
    DeathDate,
    Remark,
};

enum class EditableFieldId : std::uint8_t {
    Unspecified = 255,
    EmployeeNo = 128,
    FullName,
    PinyinSortKey,
    NationalId,
    Sex,
    Ethnicity,
    BirthDate,
    OriginalOrganization,
    Phone,
    HomeAddress,
    RetirementDate,
    PersonnelCategory,
    CadreRank,
    ProfessionalTitle,
    PositionTitle,
    Education,
    Degree,
    WorkStartDate,
    PartyBranch,
    PartyFullMemberDate,
    NativePlace,
    RelativePhone,
    IdentityCategory,
    PoliticalAffiliation,
    PartyJoinDate,
    LifeStatus,
    DeathDate,
    Remark,
};

// Domain-local values are not PersonFieldId identities or persisted field keys.
// Only these named mappings may cross the import/edit/person interfaces.

inline bool try_to_person_field(ImportFieldId field, FieldId* out) {
    if (out == nullptr) { return false; }
    switch (field) {
        case ImportFieldId::EmployeeNo: *out = FieldId::EmployeeNo; return true;
        case ImportFieldId::FullName: *out = FieldId::FullName; return true;
        case ImportFieldId::NationalId: *out = FieldId::NationalId; return true;
        case ImportFieldId::Sex: *out = FieldId::Sex; return true;
        case ImportFieldId::Ethnicity: *out = FieldId::Ethnicity; return true;
        case ImportFieldId::BirthDate: *out = FieldId::BirthDate; return true;
        case ImportFieldId::OriginalOrganization: *out = FieldId::OriginalOrganization; return true;
        case ImportFieldId::Phone: *out = FieldId::Phone; return true;
        case ImportFieldId::HomeAddress: *out = FieldId::HomeAddress; return true;
        case ImportFieldId::RetirementDate: *out = FieldId::RetirementDate; return true;
        case ImportFieldId::PersonnelCategory: *out = FieldId::PersonnelCategory; return true;
        case ImportFieldId::CadreRank: *out = FieldId::CadreRank; return true;
        case ImportFieldId::ProfessionalTitle: *out = FieldId::ProfessionalTitle; return true;
        case ImportFieldId::PositionTitle: *out = FieldId::PositionTitle; return true;
        case ImportFieldId::Education: *out = FieldId::Education; return true;
        case ImportFieldId::Degree: *out = FieldId::Degree; return true;
        case ImportFieldId::WorkStartDate: *out = FieldId::WorkStartDate; return true;
        case ImportFieldId::PartyBranch: *out = FieldId::PartyBranch; return true;
        case ImportFieldId::PartyFullMemberDate: *out = FieldId::PartyFullMemberDate; return true;
        case ImportFieldId::NativePlace: *out = FieldId::NativePlace; return true;
        case ImportFieldId::RelativePhone: *out = FieldId::RelativePhone; return true;
        case ImportFieldId::IdentityCategory: *out = FieldId::IdentityCategory; return true;
        case ImportFieldId::PoliticalAffiliation: *out = FieldId::PoliticalAffiliation; return true;
        case ImportFieldId::PartyJoinDate: *out = FieldId::PartyJoinDate; return true;
        case ImportFieldId::LifeStatus: *out = FieldId::LifeStatus; return true;
        case ImportFieldId::DeathDate: *out = FieldId::DeathDate; return true;
        case ImportFieldId::Remark: *out = FieldId::Remark; return true;
        default: return false;  // Unspecified and forged values leave output unchanged.
    }
}


inline bool try_to_person_field(EditableFieldId field, FieldId* out) {
    if (out == nullptr) { return false; }
    switch (field) {
        case EditableFieldId::EmployeeNo: *out = FieldId::EmployeeNo; return true;
        case EditableFieldId::FullName: *out = FieldId::FullName; return true;
        case EditableFieldId::PinyinSortKey: *out = FieldId::PinyinSortKey; return true;
        case EditableFieldId::NationalId: *out = FieldId::NationalId; return true;
        case EditableFieldId::Sex: *out = FieldId::Sex; return true;
        case EditableFieldId::Ethnicity: *out = FieldId::Ethnicity; return true;
        case EditableFieldId::BirthDate: *out = FieldId::BirthDate; return true;
        case EditableFieldId::OriginalOrganization: *out = FieldId::OriginalOrganization; return true;
        case EditableFieldId::Phone: *out = FieldId::Phone; return true;
        case EditableFieldId::HomeAddress: *out = FieldId::HomeAddress; return true;
        case EditableFieldId::RetirementDate: *out = FieldId::RetirementDate; return true;
        case EditableFieldId::PersonnelCategory: *out = FieldId::PersonnelCategory; return true;
        case EditableFieldId::CadreRank: *out = FieldId::CadreRank; return true;
        case EditableFieldId::ProfessionalTitle: *out = FieldId::ProfessionalTitle; return true;
        case EditableFieldId::PositionTitle: *out = FieldId::PositionTitle; return true;
        case EditableFieldId::Education: *out = FieldId::Education; return true;
        case EditableFieldId::Degree: *out = FieldId::Degree; return true;
        case EditableFieldId::WorkStartDate: *out = FieldId::WorkStartDate; return true;
        case EditableFieldId::PartyBranch: *out = FieldId::PartyBranch; return true;
        case EditableFieldId::PartyFullMemberDate: *out = FieldId::PartyFullMemberDate; return true;
        case EditableFieldId::NativePlace: *out = FieldId::NativePlace; return true;
        case EditableFieldId::RelativePhone: *out = FieldId::RelativePhone; return true;
        case EditableFieldId::IdentityCategory: *out = FieldId::IdentityCategory; return true;
        case EditableFieldId::PoliticalAffiliation: *out = FieldId::PoliticalAffiliation; return true;
        case EditableFieldId::PartyJoinDate: *out = FieldId::PartyJoinDate; return true;
        case EditableFieldId::LifeStatus: *out = FieldId::LifeStatus; return true;
        case EditableFieldId::DeathDate: *out = FieldId::DeathDate; return true;
        case EditableFieldId::Remark: *out = FieldId::Remark; return true;
        default: return false;  // Unspecified and forged values leave output unchanged.
    }
}


struct AuditFields {
    UtcTimestamp created_at;
    UtcTimestamp updated_at;
    ImportBatchId import_batch_id;
    UserId last_modified_by;
};

// This is the complete stored person shape. Derived values such as age, party
// seniority and list serial number are intentionally absent: callers compute
// them from dates or list context and must never persist them as source data.
struct PersonRecord {
    PersonId person_id;
    PersonCode person_code;  // User-visible fixed roster number; not the source employee number.
    std::string employee_no;
    std::string full_name;
    std::string pinyin_sort_key;
    std::string national_id;

    std::string sex;
    std::string ethnicity;
    LocalDate birth_date;
    std::string original_organization;
    std::string phone;
    std::string home_address;

    LocalDate retirement_date;
    std::string personnel_category;
    std::string cadre_rank;
    std::string professional_title;
    std::string position_title;
    std::string education;
    std::string degree;
    DateValue work_start_date;
    std::string party_branch;
    DateValue party_full_member_date;
    std::string native_place;
    std::string relative_phone;
    std::string identity_category;

    std::string political_affiliation;
    LocalDate party_join_date;
    LifeStatus life_status = LifeStatus::Unknown;
    LocalDate death_date;

    std::string remark;
    AuditFields audit;
};

// Request input excludes IDs, the initially generated pinyin key, and audit fields.
struct PersonCreateInput {
    std::string employee_no;
    std::string full_name;
    std::string national_id;

    std::string sex;
    std::string ethnicity;
    LocalDate birth_date;
    std::string original_organization;
    std::string phone;
    std::string home_address;

    LocalDate retirement_date;
    std::string personnel_category;
    std::string cadre_rank;
    std::string professional_title;
    std::string position_title;
    std::string education;
    std::string degree;
    DateValue work_start_date;
    std::string party_branch;
    DateValue party_full_member_date;
    std::string native_place;
    std::string relative_phone;
    std::string identity_category;

    std::string political_affiliation;
    LocalDate party_join_date;
    LifeStatus life_status = LifeStatus::Unknown;
    LocalDate death_date;

    std::string remark;
};

struct TagMutation {
    TagCode tag_code;
    std::string tag_value;
    std::int32_t applicable_year = 0;
    bool remove = false;
};

struct TagRecord {
    PersonId person_id;
    TagCode tag_code;
    std::string tag_value;
    std::int32_t applicable_year = 0;  // 0 = not year scoped; condolence uses a year.
    UtcTimestamp updated_at;
    UserId updated_by;
};

// Explicitly models the difference between an empty value and an unchanged
// value. It is the only permitted shape for partial person updates.
struct FieldChange {
    EditableFieldId field = EditableFieldId::Unspecified;
    std::string value;
    bool clear_value = false;
    DateValue date_value;  // Date fields use this; text is not an implicit date parser.
};

inline bool is_valid_field_change(const FieldChange& change) {
    FieldId field;
    if (!try_to_person_field(change.field, &field)) { return false; }
    const auto* spec = find_person_field(field);
    if (spec == nullptr || !spec->user_editable || spec->system_managed) { return false; }
    const bool empty_date = change.date_value.precision == DatePrecision::Unknown &&
        change.date_value.is_valid();
    // Identifier/Timestamp cannot become editable, even with a future metadata mistake.
    if (spec->value_kind == FieldValueKind::Identifier ||
        spec->value_kind == FieldValueKind::Timestamp) { return false; }
    if (change.clear_value) { return change.value.empty() && empty_date; }
    switch (spec->value_kind) {
        case FieldValueKind::Date:
            return change.value.empty() && change.date_value.is_known();
        case FieldValueKind::Text:
        case FieldValueKind::EnumCode:
            return empty_date;  // Required values/code vocabularies are checked by D3.
        default:
            return false;
    }
}

struct PersonEditInput {
    std::vector<FieldChange> changes;
};

enum class ImportColumnDisposition : std::uint8_t { PersonField, BatchRawOnly, Unsupported };

struct ImportColumnBinding {
    std::size_t source_column_index = 0;
    std::string source_column_name;
    ImportFieldId target_field = ImportFieldId::Unspecified;
    bool required = false;
    ImportColumnDisposition disposition = ImportColumnDisposition::Unsupported;
    bool status_source_confirmed = false;  // Explicit mapping confirmation for a status column.
};

inline bool is_valid_import_binding(const ImportColumnBinding& binding) {
    if (binding.disposition == ImportColumnDisposition::BatchRawOnly) {
        return binding.target_field == ImportFieldId::Unspecified;
    }
    if (binding.disposition != ImportColumnDisposition::PersonField) { return false; }
    FieldId field;
    if (!try_to_person_field(binding.target_field, &field)) { return false; }
    const auto* spec = find_person_field(field);
    return spec != nullptr && spec->source_importable && !spec->system_managed &&
        (binding.target_field != ImportFieldId::LifeStatus || binding.status_source_confirmed);
}

enum class StatusSource : std::uint8_t { Unresolved, SourceColumn, ConfirmedBatchDefault, FrozenProfile, Mixed };

struct ImportStatusResolution {
    StatusSource source = StatusSource::Unresolved;
    LifeStatus fallback_status = LifeStatus::Unknown;
    bool fallback_confirmed = false;
};

struct ImportProfile {
    std::string profile_id;
    std::uint32_t version = 0;
    std::size_t header_row_number = 0;
    std::vector<ImportColumnBinding> column_bindings;
    ImportStatusResolution status_resolution;

};

enum class ImportErrorCode : std::uint8_t {
    MissingRequiredValue,
    InvalidDate,
    InvalidEnumCode,
    DuplicateCandidate,
    UnknownColumn,
    UnsupportedWorkbook,
    UnresolvedLifeStatus,
    AmbiguousColumn,
    UnsupportedColumn,
};

struct ImportIssue {
    ImportErrorCode code = ImportErrorCode::MissingRequiredValue;
    std::string source_file_name;
    std::string worksheet_name;
    std::size_t source_row_number = 0;
    FieldId field = FieldId::FullName;
    std::string original_value;
    std::string message;
};

struct ImportPreview {
    ImportBatchId batch_id;
    PreviewRevision preview_revision;
    std::string source_sha256;  // Computed by the service from the checked source content.
    std::string source_file_name;
    std::string worksheet_name;
    std::size_t source_record_count = 0;
    std::size_t valid_record_count = 0;
    std::size_t invalid_record_count = 0;
    std::size_t duplicate_candidate_count = 0;
    std::size_t unresolved_duplicate_count = 0;
    std::string profile_id;
    std::uint32_t profile_version = 0;
    std::uint32_t mapping_version = 0;
    ImportStatusResolution status_resolution;
    std::vector<ImportColumnBinding> column_bindings;
    std::vector<ImportIssue> issues;
};

// BatchRawOnly cells are private local import data, never public evidence or logs.
struct ImportRawCell {
    ImportBatchId batch_id;
    std::size_t source_row_number = 0;
    std::size_t source_column_index = 0;
    std::string source_column_name;
    std::string original_value;
};

struct ImportBatchRecord {
    ImportBatchId batch_id;
    PreviewRevision preview_revision;
    std::string source_sha256;
    std::string source_file_name;  // Basename only; no permanent sensitive absolute path.
    std::string worksheet_name;
    std::size_t source_record_count = 0;
    std::size_t valid_record_count = 0;
    std::size_t imported_record_count = 0;
    std::size_t invalid_record_count = 0;
    std::size_t duplicate_candidate_count = 0;
    std::string profile_id;
    std::uint32_t profile_version = 0;
    std::uint32_t mapping_version = 0;
    ImportStatusResolution status_resolution;
    UtcTimestamp executed_at;
    UserId executed_by;
};

enum class Comparison : std::uint8_t {
    Equals,
    NotEquals,
    Contains,
    IsEmpty,
    IsNotEmpty,
    BetweenInclusive,
    GreaterThanOrEqual,
    LessThanOrEqual,
};

struct FieldCondition {
    FieldId field = FieldId::FullName;
    Comparison comparison = Comparison::Equals;
    std::string first_value;
    std::string second_value;
};

enum class MatchMode : std::uint8_t { All, Any };
enum class RosterScenario : std::uint8_t { Custom, Chongyang, Party50 };
enum class LifeStatusFilter : std::uint8_t { Unspecified, LivingOnly, DeceasedOnly, All };
enum class AgeBasis : std::uint8_t { CompletedAge, CalendarYearAge };

// accepted_values OR inclusive lower bound, applied only when enabled.
struct YearCountCondition {
    bool enabled = false;
    std::vector<std::int32_t> accepted_values;
    bool has_minimum = false;
    std::int32_t minimum = 0;
};

// Shape only: no age calculation, scenario expansion or row selection.
inline bool is_valid_year_count_condition(const YearCountCondition& condition) {
    if (!condition.enabled) { return true; }
    if (condition.accepted_values.empty() && !condition.has_minimum) { return false; }
    if (condition.minimum < 0) { return false; }
    for (auto value : condition.accepted_values) {
        if (value < 0) { return false; }
    }
    return true;
}

struct TagCondition {
    TagCode tag_code;
    std::string tag_value;
    std::int32_t applicable_year = 0;
};

struct FilterSpec {
    FilterId filter_id;
    std::string display_name;
    std::int32_t target_year = 0;
    DateValue as_of_date;  // FullDate required; UI supplies today, tests a fixed date.
    RosterScenario scenario = RosterScenario::Custom;
    LifeStatusFilter life_status = LifeStatusFilter::Unspecified;
    AgeBasis age_basis = AgeBasis::CalendarYearAge;
    YearCountCondition age;
    YearCountCondition party_seniority;
    bool require_party_member = false;
    MatchMode field_match = MatchMode::All;
    std::vector<FieldCondition> conditions;
    MatchMode tag_match = MatchMode::All;
    std::vector<TagCondition> tags;
};

struct RosterRow {
    PersonId person_id;
    std::size_t print_serial_number = 0;
    PersonRecord person;
    std::vector<TagRecord> tags;  // Same data version as person; output never refetches tags.
    std::int32_t completed_age = -1;
    std::int32_t calendar_year_age = -1;
    std::int32_t party_seniority_years = -1;
};

struct RosterResult {
    SnapshotId snapshot_id;
    DataVersion data_version = 0;
    UtcTimestamp generated_at;
    FilterSpec filter_spec;  // Resolved scenario conditions, for display/audit only.
    std::vector<RosterRow> rows;
    std::size_t total_count() const { return rows.size(); }
};

enum class DerivedColumnId : std::uint8_t {
    PrintSerialNumber, CompletedAge, CalendarYearAge, PartySeniorityYears,
};
enum class TemplateColumnSource : std::uint8_t {
    PersonField, DerivedField, BlankSignature, StaticText,
};

struct TemplateColumn {
    TemplateColumnSource source = TemplateColumnSource::PersonField;
    FieldId field = FieldId::FullName;
    DerivedColumnId derived_field = DerivedColumnId::PrintSerialNumber;
    std::string static_text;
    std::string display_name;
    std::uint16_t width_tenth_mm = 200;
    bool visible = true;
};

enum class PaperSize : std::uint8_t { A4 };
enum class PageOrientation : std::uint8_t { Portrait, Landscape };
enum class PageNumberPolicy : std::uint8_t { None, CurrentAndTotal };

struct PageMargins {
    // Draft UI suggestions; effective parameters require business/template validation.
    std::uint16_t left_tenth_mm = 150;
    std::uint16_t right_tenth_mm = 150;
    std::uint16_t top_tenth_mm = 150;
    std::uint16_t bottom_tenth_mm = 150;
};

struct PrintTemplate {
    TemplateId template_id;
    std::uint32_t template_version = 0;
    std::string template_name;
    std::string title;
    std::vector<TemplateColumn> columns;
    std::uint16_t font_size_pt = 12;
    std::uint16_t title_font_size_pt = 18;
    std::uint16_t header_font_size_pt = 12;
    PaperSize paper_size = PaperSize::A4;
    PageOrientation orientation = PageOrientation::Portrait;
    PageMargins margins;
    std::uint16_t row_height_tenth_mm = 100;
    std::uint16_t rows_per_page = 0;
    bool repeat_header = true;
    PageNumberPolicy page_number_policy = PageNumberPolicy::CurrentAndTotal;
};

// Application service resolves the same snapshot for all adapters and rejects
// a stale data_version before output. The service publishes const copies.
struct PrintModel {
    std::shared_ptr<const RosterResult> roster;
    std::shared_ptr<const PrintTemplate> print_template;
};

enum class ExportResult : std::uint8_t { Succeeded, Failed };
struct ExportLogRecord {
    ExportId export_id;
    SnapshotId snapshot_id;
    TemplateId template_id;
    std::uint32_t template_version = 0;
    std::string filter_summary;  // Redacted summary; no raw sensitive field values.
    std::size_t record_count = 0;
    std::string output_path;  // Real path in private local storage; redact display/public evidence.
    UtcTimestamp created_at;
    UserId requested_by;
    ExportResult result = ExportResult::Failed;
};

enum class ApiErrorCode : std::uint16_t {
    ContractVersionMismatch,
    ValidationFailed,
    NotFound,
    Conflict,
    ImportConfirmationRequired,
    BackupFailed,
    RestoreFailed,
    ExportFailed,
    StaleSnapshot,
    InvalidTemplate,
    InternalError,
};

struct ApiError {
    ApiErrorCode code = ApiErrorCode::InternalError;
    std::string message;
    FieldId field = FieldId::FullName;
    bool has_field = false;
    std::size_t source_row_number = 0;
    bool has_source_row = false;
};

struct ApiMeta {
    ContractVersion contract_version = kCurrentContractVersion;
    RequestId request_id;
};

template <typename T>
struct ApiResult {
    ApiMeta meta;
    bool ok = false;
    T data;
    std::vector<ApiError> errors;
};

struct ImportPreviewRequest {
    // Untrusted proposal: the service revalidates source, profile, bindings and status.
    // Caller versions are hints, never approval evidence or the trusted preview identity.
    ApiMeta meta;
    std::string source_file_path;
    std::string worksheet_name;
    std::vector<ImportColumnBinding> column_bindings;
    std::string profile_id;
    std::uint32_t profile_version = 0;
    std::uint32_t mapping_version = 0;
    ImportStatusResolution status_resolution;
};

struct ConfirmImportRequest {
    // Load the service-owned preview by both identities; never re-read caller semantics.
    ApiMeta meta;
    ImportBatchId batch_id;
    PreviewRevision preview_revision;
    UserId confirmed_by;
};

struct CreatePersonRequest {
    ApiMeta meta;
    PersonCreateInput person;
    UserId created_by;
};

struct UpdatePersonRequest {
    ApiMeta meta;
    PersonId person_id;
    PersonEditInput input;
    UserId changed_by;
};

struct UpdateTagRequest {
    ApiMeta meta;
    PersonId person_id;
    TagMutation mutation;
    UserId changed_by;
};

struct SearchPeopleRequest {
    ApiMeta meta;
    std::string search_text;
    FilterSpec filter;
};

struct GenerateRosterRequest {
    ApiMeta meta;
    FilterSpec filter;
};

struct ExportRosterRequest {
    ApiMeta meta;
    SnapshotId snapshot_id;
    PrintTemplate print_template;
    std::string output_file_path;
    UserId requested_by;
};

struct PreviewRosterRequest {
    ApiMeta meta;
    SnapshotId snapshot_id;
    PrintTemplate print_template;  // Value copy of the chosen template version.
};

struct PrintRosterRequest {
    ApiMeta meta;
    SnapshotId snapshot_id;
    PrintTemplate print_template;
    UserId requested_by;
};

struct BackupRequest {
    ApiMeta meta;
    std::string backup_directory;
    UserId requested_by;
};

struct RestoreRequest {
    ApiMeta meta;
    std::string backup_file_path;
    UserId requested_by;
};

}  // namespace schema
}  // namespace retiree_roster
