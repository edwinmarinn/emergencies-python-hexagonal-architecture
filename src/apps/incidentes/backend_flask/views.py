from dependency_injector.wiring import Provide
from flask import request

from apps.incidentes.__dependency_injection import Container
from contexts.incidentes.emergencias.application.create import CreateEmergenciaCommand
from contexts.incidentes.emergencias.application.find import FindEmergenciaQuery
from contexts.incidentes.emergencias.application.list import ListEmergenciasQuery
from contexts.shared.domain.bus.command import CommandBus
from contexts.shared.domain.bus.query import QueryBus


async def create_emergencia(command_bus: CommandBus = Provide[Container.command_bus]):
    data = request.get_json()
    command = CreateEmergenciaCommand(
        id=data["id"], abscisa=int(data["abscisa"]), user_id=data["user_id"]
    )
    await command_bus.dispatch(command)
    return {}


async def find_emergencia(
    emergencia_id, query_bus: QueryBus = Provide[Container.query_bus]
):
    query = FindEmergenciaQuery(emergencia_id)
    emergencia = await query_bus.ask(query)

    if emergencia:
        return emergencia.__dict__
    return {}


async def list_emergencia(query_bus: QueryBus = Provide[Container.query_bus]):
    query = ListEmergenciasQuery(
        filters="", order_by="id", order_type="asc", offset=0, limit=10
    )
    emergencias = await query_bus.ask(query)

    return emergencias.__dict__
