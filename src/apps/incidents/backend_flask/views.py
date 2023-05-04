from dependency_injector.wiring import Provide
from flask import request

from apps.incidents.__dependency_injection import Container
from contexts.incidents.emergencies.application.create import CreateEmergencyCommand
from contexts.incidents.emergencies.application.find import FindEmergencyQuery
from contexts.incidents.emergencies.application.list import ListEmergenciesQuery
from contexts.shared.domain.bus.command import CommandBus
from contexts.shared.domain.bus.query import QueryBus


async def create_emergency(command_bus: CommandBus = Provide[Container.command_bus]):
    data = request.get_json()
    command = CreateEmergencyCommand(
        id=data["id"], abscissa=int(data["abscissa"]), user_id=data["user_id"]
    )
    await command_bus.dispatch(command)
    return {}


async def find_emergency(
    emergency_id, query_bus: QueryBus = Provide[Container.query_bus]
):
    query = FindEmergencyQuery(emergency_id)
    emergency = await query_bus.ask(query)

    if emergency:
        return emergency.__dict__
    return {}


async def list_emergency(query_bus: QueryBus = Provide[Container.query_bus]):
    query = ListEmergenciesQuery(
        filters="", order_by="id", order_type="asc", offset=0, limit=10
    )
    emergencies = await query_bus.ask(query)

    return emergencies.__dict__
