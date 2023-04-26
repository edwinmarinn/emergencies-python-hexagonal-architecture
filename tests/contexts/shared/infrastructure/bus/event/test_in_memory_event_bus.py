import pytest
from pytest_asyncio import fixture

from contexts.shared.infrastructure.bus.event import InMemoryEventBus


@fixture
def in_memory_event_bus(fake_domain_event_subscriber) -> InMemoryEventBus:
    return InMemoryEventBus([fake_domain_event_subscriber])


class TestInMemoryEventBus:
    def test_should_return_a_response_successfully_on_fake_domain_event_one(
        self, in_memory_event_bus, fake_domain_event_one
    ):
        with pytest.raises(RuntimeError, match="This works fine!"):
            in_memory_event_bus.publish(fake_domain_event_one)

    def test_should_return_a_response_successfully_on_fake_domain_event_two(
        self, in_memory_event_bus, fake_domain_event_two
    ):
        with pytest.raises(RuntimeError, match="This works fine!"):
            in_memory_event_bus.publish(fake_domain_event_two)
