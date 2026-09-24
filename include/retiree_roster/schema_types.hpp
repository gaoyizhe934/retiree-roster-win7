#pragma once

#include <array>
#include <cstddef>
#include <cstdint>
#include <string>
#include <utility>
#include <vector>

// This header is the single field contract for UI, application services,
// SQLite adapters, xlsx adapters, print templates, and all API DTOs.
// It deliberately uses only C++14 standard-library types for the Win7 target.
namespace retiree_roster {
namespace schema {

using SchemaVersion = std::uint32_t;
constexpr SchemaVersion kCurrentSchemaVersion = 1U;

using PersonId = std::string;
using ImportBatchId = std::string;
using TemplateId = std::string;
using FilterId = std::string;
using RequestId = std::string;
using UserId = std::string;

// An empty date means "unknown". Do not overload 1900-01-01 or another real date.
struct LocalDate {
    std::int32_t year = 0;
    std::uint8_t month = 0;
    std::uint8_t day = 0;

    bool is_known() const {
        return year > 0 && month >= 1U && month <= 12U && day >= 1U && day <= 31U;
    }
};

// ISO-8601 UTC text, for example "2026-09-21T08:30:00Z".
// A string is intentional: C++14 has no standard time-zone type.
using UtcTimestamp = std::string;

enum class LifeStatus : std::uint8_t {
    Living,
    Deceased,
};

enum class FieldValueKind : std::uint8_t {
    Text,
    Date,
    Boolean,
    EnumCode,
    Identifier,
    Timestamp,
    TagCollection,
};

// FieldId is the canonical API/database/template identity. Do not pass free-form
// field keys between modules; map source headings to this enum during import.
enum class FieldId : std::uint8_t {
    PersonId,
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
    JobTitle,
    PoliticalAffiliation,
    PartyJoinDate,
    LifeStatus,
    DeathDate,
    HasFinancialDifficulty,
    HasLongTermIllness,
    IsHighAgeMarked,
    HasReceivedCondolenceThisYear,
    Remark,
    TagCodes,
    CreatedAt,
    UpdatedAt,
    ImportBatchId,
    LastModifiedBy,
};

struct FieldSpec {
    FieldId id;
    const char* key;
    FieldValueKind value_kind;
    bool required_for_import;
    bool sensitive;
    bool mutable_after_create;
    bool printable_by_default;
};

inline const std::array<FieldSpec, 29>& person_field_specs() {
    static const std::array<FieldSpec, 29> kSpecs = {{
        {FieldId::PersonId, "person_id", FieldValueKind::Identifier, false, false, false, true},
        {FieldId::EmployeeNo, "employee_no", FieldValueKind::Text, false, false, true, true},
        {FieldId::FullName, "full_name", FieldValueKind::Text, true, false, true, true},
        {FieldId::PinyinSortKey, "pinyin_sort_key", FieldValueKind::Text, false, false, true, false},
        {FieldId::NationalId, "national_id", FieldValueKind::Text, false, true, true, false},
        {FieldId::Sex, "sex", FieldValueKind::EnumCode, false, false, true, true},
        {FieldId::Ethnicity, "ethnicity", FieldValueKind::Text, false, false, true, true},
        {FieldId::BirthDate, "birth_date", FieldValueKind::Date, false, false, true, true},
        {FieldId::OriginalOrganization, "original_organization", FieldValueKind::Text, false, false, true, true},
        {FieldId::Phone, "phone", FieldValueKind::Text, false, true, true, false},
        {FieldId::HomeAddress, "home_address", FieldValueKind::Text, false, true, true, false},
        {FieldId::RetirementDate, "retirement_date", FieldValueKind::Date, false, false, true, true},
        {FieldId::PersonnelCategory, "personnel_category", FieldValueKind::EnumCode, false, false, true, true},
        {FieldId::CadreRank, "cadre_rank", FieldValueKind::EnumCode, false, false, true, true},
        {FieldId::JobTitle, "job_title", FieldValueKind::Text, false, false, true, true},
        {FieldId::PoliticalAffiliation, "political_affiliation", FieldValueKind::EnumCode, false, false, true, true},
        {FieldId::PartyJoinDate, "party_join_date", FieldValueKind::Date, false, false, true, true},
        {FieldId::LifeStatus, "life_status", FieldValueKind::EnumCode, true, false, true, true},
        {FieldId::DeathDate, "death_date", FieldValueKind::Date, false, false, true, false},
        {FieldId::HasFinancialDifficulty, "has_financial_difficulty", FieldValueKind::Boolean, false, false, true, true},
        {FieldId::HasLongTermIllness, "has_long_term_illness", FieldValueKind::Boolean, false, false, true, true},
        {FieldId::IsHighAgeMarked, "is_high_age_marked", FieldValueKind::Boolean, false, false, true, false},
        {FieldId::HasReceivedCondolenceThisYear, "has_received_condolence_this_year", FieldValueKind::Boolean, false, false, true, false},
        {FieldId::Remark, "remark", FieldValueKind::Text, false, false, true, false},
        {FieldId::TagCodes, "tag_codes", FieldValueKind::TagCollection, false, false, true, false},
        {FieldId::CreatedAt, "created_at", FieldValueKind::Timestamp, false, false, false, false},
        {FieldId::UpdatedAt, "updated_at", FieldValueKind::Timestamp, false, false, false, false},
        {FieldId::ImportBatchId, "import_batch_id", FieldValueKind::Identifier, false, false, false, false},
        {FieldId::LastModifiedBy, "last_modified_by", FieldValueKind::Identifier, false, false, true, false},
    }};
    return kSpecs;
}

inline const FieldSpec* find_person_field(const std::string& key) {
    const std::array<FieldSpec, 29>& specs = person_field_specs();
    for (std::size_t i = 0; i < specs.size(); ++i) {
        if (key == specs[i].key) {
            return &specs[i];
        }
    }
    return nullptr;
}

inline const FieldSpec* find_person_field(FieldId id) {
    const std::array<FieldSpec, 29>& specs = person_field_specs();
    for (std::size_t i = 0; i < specs.size(); ++i) {
        if (id == specs[i].id) {
            return &specs[i];
        }
    }
    return nullptr;
}

inline bool is_current_schema(SchemaVersion version) {
    return version == kCurrentSchemaVersion;
}

struct CareFlags {
    bool has_financial_difficulty = false;
    bool has_long_term_illness = false;
    bool is_high_age_marked = false;
    bool has_received_condolence_this_year = false;
};

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
    std::string job_title;

    std::string political_affiliation;
    LocalDate party_join_date;
    LifeStatus life_status = LifeStatus::Living;
    LocalDate death_date;

    CareFlags care;
    std::string remark;
    AuditFields audit;
};

struct TagRecord {
    PersonId person_id;
    std::string tag_code;
    std::string tag_value;
    UtcTimestamp updated_at;
    UserId updated_by;
};

// Explicitly models the difference between an empty value and an unchanged
// value. It is the only permitted shape for partial person updates.
struct FieldChange {
    FieldId field;
    std::string value;
    bool clear_value = false;
};

struct ImportColumnBinding {
    std::size_t source_column_index = 0;
    std::string source_column_name;
    FieldId target_field = FieldId::FullName;
    bool required = false;
};

enum class ImportErrorCode : std::uint8_t {
    MissingRequiredValue,
    InvalidDate,
    InvalidEnumCode,
    DuplicateCandidate,
    UnknownColumn,
    UnsupportedWorkbook,
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
    std::string source_file_name;
    std::string worksheet_name;
    std::size_t source_record_count = 0;
    std::size_t valid_record_count = 0;
    std::size_t invalid_record_count = 0;
    std::size_t duplicate_candidate_count = 0;
    std::vector<ImportColumnBinding> column_bindings;
    std::vector<ImportIssue> issues;
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

struct FilterSpec {
    FilterId filter_id;
    std::string display_name;
    std::int32_t target_year = 0;
    bool include_deceased = false;
    std::vector<FieldCondition> conditions;
    std::vector<std::string> required_tag_codes;
};

struct RosterRow {
    PersonId person_id;
    std::size_t print_serial_number = 0;
    PersonRecord person;
    std::int32_t completed_age = -1;
    std::int32_t calendar_year_age = -1;
    std::int32_t party_seniority_years = -1;
};

struct TemplateColumn {
    FieldId field = FieldId::FullName;
    std::string display_name;
    std::uint16_t width_in_chars = 12;
    bool visible = true;
};

struct PrintTemplate {
    TemplateId template_id;
    std::string template_name;
    std::string title;
    std::vector<TemplateColumn> columns;
    std::uint16_t font_size_pt = 12;
    bool landscape = false;
    std::uint16_t rows_per_page = 0;
    bool repeat_header = true;
    bool add_signature_column = false;
    bool add_remark_column = false;
};

enum class ApiErrorCode : std::uint16_t {
    SchemaVersionMismatch,
    ValidationFailed,
    NotFound,
    Conflict,
    ImportConfirmationRequired,
    BackupFailed,
    RestoreFailed,
    ExportFailed,
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
    SchemaVersion schema_version = kCurrentSchemaVersion;
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
    ApiMeta meta;
    std::string source_file_path;
    std::string worksheet_name;
    std::vector<ImportColumnBinding> column_bindings;
};

struct ConfirmImportRequest {
    ApiMeta meta;
    ImportBatchId batch_id;
    UserId confirmed_by;
};

struct CreatePersonRequest {
    ApiMeta meta;
    PersonRecord person;
};

struct UpdatePersonRequest {
    ApiMeta meta;
    PersonId person_id;
    std::vector<FieldChange> changes;
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
    bool include_fixed_person_id = true;
};

struct ExportRosterRequest {
    ApiMeta meta;
    FilterSpec filter;
    PrintTemplate print_template;
    std::string output_file_path;
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
