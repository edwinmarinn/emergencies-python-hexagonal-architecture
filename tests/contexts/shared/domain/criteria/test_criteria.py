from contexts.shared.domain.criteria import Criteria
from contexts.shared.domain.criteria import Filter
from contexts.shared.domain.criteria import FilterField
from contexts.shared.domain.criteria import FilterOperator
from contexts.shared.domain.criteria import FilterValue
from contexts.shared.domain.criteria import Filters
from contexts.shared.domain.criteria import Order
from contexts.shared.domain.criteria import OrderBy
from contexts.shared.domain.criteria import OrderType


class TestCriteria:
    def test_should_instantiate(self):
        criteria = Criteria(
            filters=Filters(
                [
                    Filter(
                        field=FilterField("id"),
                        operator=FilterOperator("="),
                        value=FilterValue("20"),
                    ),
                    Filter.from_values(
                        {"field": "age", "operator": ">=", "value": "18"}
                    ),
                ]
            ),
            order=Order(order_by=OrderBy("id"), order_type=OrderType("asc")),
            offset=10,
            limit=100,
        )
        print("")
        print(criteria.serialize())
