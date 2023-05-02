from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from apps.incidentes.__dependency_injection import Container
from contexts.incidentes.emergencias.application.create import CreateEmergenciaCommand
from contexts.incidentes.emergencias.application.find import FindEmergenciaQuery
from contexts.incidentes.emergencias.application.list import ListEmergenciasQuery
from contexts.incidentes.emergencias_counter.application.find import (
    FindEmergenciasCounterQuery,
)
from contexts.shared.domain.bus.command import CommandBus
from contexts.shared.domain.bus.query import QueryBus

router = APIRouter()


class EmergenciaBody(BaseModel):
    id: str
    abscisa: int
    usuario_id: str


@router.put("/emergencias/")
@inject
async def create_emergencia(
    emergencia: EmergenciaBody,
    command_bus: CommandBus = Depends(Provide[Container.command_bus]),
):
    command = CreateEmergenciaCommand(
        id=emergencia.id, abscisa=emergencia.abscisa, usuario_id=emergencia.usuario_id
    )
    await command_bus.dispatch(command)
    return {}


@router.get("/emergencias/<emergencia_id>")
@inject
async def find_emergencia(
    emergencia_id, query_bus: QueryBus = Depends(Provide[Container.query_bus])
):
    query = FindEmergenciaQuery(emergencia_id)
    emergencia = await query_bus.ask(query)

    if emergencia:
        return emergencia.__dict__
    return {}


@router.get("/emergencias/")
@inject
async def list_emergencia(query_bus: QueryBus = Depends(Provide[Container.query_bus])):
    query = ListEmergenciasQuery(
        filters="", order_by="id", order_type="asc", offset=0, limit=10
    )
    emergencias = await query_bus.ask(query)

    return emergencias.__dict__


@router.get("/emergencias/count")
@inject
async def count_emergencias(
    query_bus: QueryBus = Depends(Provide[Container.query_bus]),
):
    query = FindEmergenciasCounterQuery()
    count = await query_bus.ask(query)
    return count.__dict__
