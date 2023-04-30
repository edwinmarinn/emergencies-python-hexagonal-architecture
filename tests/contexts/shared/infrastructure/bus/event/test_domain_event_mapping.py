import pytest

from contexts.shared.infrastructure.bus.event.domain_event_mapping import (
    DomainEventMapping,
)
from tests.contexts.shared.infrastructure.bus.event.__mocks__ import (
    FakeDomainEventOne,
    FakeDomainEventTwo,
)


class TestDomainEventMapping:
    def test_should_map_events_names_to_classes(self, fake_domain_event_subscriber):
        domain_event_mapping = DomainEventMapping([fake_domain_event_subscriber])
        assert domain_event_mapping["fake_domain_event_one"] == FakeDomainEventOne
        assert domain_event_mapping["fake_domain_event_two"] == FakeDomainEventTwo

    def test_should_raise_key_error(self, fake_domain_event_subscriber):
        domain_event_mapping = DomainEventMapping([fake_domain_event_subscriber])
        with pytest.raises(KeyError):
            _ = domain_event_mapping["non_existent_domain_event"]

    def test_should_return_none(self, fake_domain_event_subscriber):
        domain_event_mapping = DomainEventMapping([fake_domain_event_subscriber])
        assert domain_event_mapping.get("non_existent_domain_event") is None
