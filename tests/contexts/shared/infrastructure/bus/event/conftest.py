from pytest_asyncio import fixture

from tests.contexts.shared.domain.uuuid_mother import UuidMother
from tests.contexts.shared.infrastructure.bus.event.__mocks__ import (
    FakeDomainEventOne,
    FakeDomainEventSubscriber,
    FakeDomainEventTwo,
)


@fixture
def fake_domain_event_one():
    return FakeDomainEventOne(aggregate_id=UuidMother.random())


@fixture
def fake_domain_event_two():
    return FakeDomainEventTwo(aggregate_id=UuidMother.random())


@fixture
def fake_domain_event_subscriber():
    return FakeDomainEventSubscriber()
