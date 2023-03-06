from contexts.shared.domain.criteria import (
    Criteria,
    Filter,
    FilterField,
    FilterOperator,
    Filters,
    FilterValue,
    Order,
    OrderBy,
    OrderType,
)


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
                    Filter(
                        field=FilterField("age"),
                        operator=FilterOperator(">="),
                        value=FilterValue("18"),
                    ),
                ]
            ),
            order=Order(order_by=OrderBy("id"), order_type=OrderType("asc")),
            offset=10,
            limit=100,
        )

    def test_should_instantiate_from_values(self):
        criteria = Criteria(
            filters=Filters.from_values(
                [
                    {"field": "id", "operator": "=", "value": "20"},
                    {"field": "age", "operator": ">=", "value": "18"},
                    {"field": "age", "operator": ">=", "value": "18"},
                ]
            ),
            order=Order(order_by=OrderBy("id"), order_type=OrderType("asc")),
            offset=10,
            limit=100,
        )
