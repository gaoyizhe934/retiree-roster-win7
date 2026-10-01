#include "retiree_roster/schema_types.hpp"
#include <cassert>

using namespace retiree_roster::schema;

int main() {
    DateValue unknown;
    assert(unknown.is_valid() && !unknown.is_known());
    DateValue year{1950, 0, 0, DatePrecision::Year};
    assert(year.is_valid() && year.is_known() && !year.is_full_date());
    DateValue month{1950, 6, 0, DatePrecision::YearMonth};
    assert(month.is_valid() && !month.is_full_date());
    DateValue birthday{1950, 6, 18, DatePrecision::FullDate};
    assert(birthday.is_valid() && birthday.is_full_date());
    DateValue invalid{1950, 2, 29, DatePrecision::FullDate};
    assert(!invalid.is_valid());
    DateValue leap{2000, 2, 29, DatePrecision::FullDate};
    assert(leap.is_valid());
    DateValue century{1900, 2, 29, DatePrecision::FullDate};
    assert(!century.is_valid());
    DateValue invented_day{1950, 6, 1, DatePrecision::YearMonth};
    assert(!invented_day.is_valid());
    DateValue missing_day{1950, 6, 0, DatePrecision::FullDate};
    assert(!missing_day.is_valid() && !missing_day.is_full_date());
    DateValue malformed_unknown{1950, 0, 0, DatePrecision::Unknown};
    assert(!malformed_unknown.is_valid() && !malformed_unknown.is_known());
}
