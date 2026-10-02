#include "retiree_roster/schema_types.hpp"
#include <cassert>

using namespace retiree_roster::schema;

int main() {
    YearCountCondition condition;
    assert(is_valid_year_count_condition(condition));
    condition.enabled = true;
    assert(!is_valid_year_count_condition(condition));
    condition.accepted_values = {70, 75, 80, 85};
    assert(is_valid_year_count_condition(condition));
    condition.accepted_values.clear();
    condition.has_minimum = true;
    condition.minimum = 90;
    assert(is_valid_year_count_condition(condition));
    condition.accepted_values = {70, 75, 80, 85};
    assert(is_valid_year_count_condition(condition));
    condition.accepted_values.push_back(-1);
    assert(!is_valid_year_count_condition(condition));
    condition.accepted_values.clear();
    condition.minimum = -1;
    assert(!is_valid_year_count_condition(condition));
    condition.has_minimum = false;
    condition.accepted_values = {50};
    assert(!is_valid_year_count_condition(condition));  // Negative stored minimum is malformed.
    condition.enabled = false;
    assert(is_valid_year_count_condition(condition));  // Disabled values do not constrain a query.
}
