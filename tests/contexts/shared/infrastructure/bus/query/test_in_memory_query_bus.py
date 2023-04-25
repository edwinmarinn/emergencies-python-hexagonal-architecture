from typing import Type

import pytest
from pytest import fixture

from contexts.shared.domain.bus.query import (
    Query,
    QueryHandler,
    QueryNotRegisteredError,
)
from contexts.shared.infrastructure.bus.query import InMemoryQueryBus


class FakeQuery(Query):
    pass


class FakeQueryHandler(QueryHandler):
    def subscribed_to(self) -> Type[Query]:
        return FakeQuery

    def __call__(self, query: FakeQuery):
        raise RuntimeError("This works fine!")


class NotRegisteredQuery(Query):
    pass


@fixture
def in_memory_query_bus() -> InMemoryQueryBus:
    bus = InMemoryQueryBus([FakeQueryHandler()])
    return bus


class TestSimpleQueryBus:
    @pytest.mark.asyncio
    async def test_should_return_a_response_successfully(self, in_memory_query_bus):
        with pytest.raises(RuntimeError, match="This works fine!"):
            await in_memory_query_bus.ask(FakeQuery())

    @pytest.mark.asyncio
    async def test_should_raise_an_exception_dispatching_a_non_registered_query(
        self, in_memory_query_bus
    ):
        with pytest.raises(QueryNotRegisteredError):
            await in_memory_query_bus.ask(NotRegisteredQuery())
