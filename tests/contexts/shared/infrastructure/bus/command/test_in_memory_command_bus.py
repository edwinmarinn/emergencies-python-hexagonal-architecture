import pytest
from pytest import fixture

from contexts.shared.domain.bus.command import (
    Command,
    CommandHandler,
    CommandNotRegisteredError,
)
from contexts.shared.infrastructure.bus.command import InMemoryCommandBus


class FakeCommand(Command):
    pass


class FakeCommandHandler(CommandHandler):
    async def __call__(self, command: FakeCommand):
        raise RuntimeError("This works fine!")


class NotRegisteredCommand(Command):
    pass


@fixture
def in_memory_command_bus() -> InMemoryCommandBus:
    bus = InMemoryCommandBus([FakeCommandHandler()])
    return bus


class TestSimpleCommandBus:
    @pytest.mark.asyncio
    async def test_should_return_a_response_successfully(self, in_memory_command_bus):
        with pytest.raises(RuntimeError, match="This works fine!"):
            await in_memory_command_bus.dispatch(FakeCommand())

    @pytest.mark.asyncio
    async def test_should_raise_an_exception_dispatching_a_non_registered_command(
        self, in_memory_command_bus
    ):
        with pytest.raises(CommandNotRegisteredError):
            await in_memory_command_bus.dispatch(NotRegisteredCommand())
