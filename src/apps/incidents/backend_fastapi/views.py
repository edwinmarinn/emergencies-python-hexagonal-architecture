from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from apps.incidents.__dependency_injection import Container
from contexts.incidents.emergencies.application.create import CreateEmergencyCommand
from contexts.incidents.emergencies.application.find import FindEmergencyQuery
from contexts.incidents.emergencies.application.list import ListEmergenciesQuery
from contexts.incidents.emergencies_counter.application.find import (
    FindEmergenciesCounterQuery,
)
from contexts.incidents.emergencies_counter_per_user.application.find import (
    FindEmergenciesCounterPerUserQuery,
)
from contexts.shared.domain.bus.command import CommandBus
from contexts.shared.domain.bus.query import QueryBus

router = APIRouter()


class EmergencyBody(BaseModel):
    id: str
    abscissa: int
    user_id: str


@router.put("/emergencies/")
@inject
async def create_emergency(
    emergency: EmergencyBody,
    command_bus: CommandBus = Depends(Provide[Container.command_bus]),
):
    command = CreateEmergencyCommand(
        id=emergency.id, abscissa=emergency.abscissa, user_id=emergency.user_id
    )
    await command_bus.dispatch(command)
    return {}


@router.get("/emergencies/")
@inject
async def list_emergency(query_bus: QueryBus = Depends(Provide[Container.query_bus])):
    query = ListEmergenciesQuery(
        filters="", order_by="id", order_type="asc", offset=0, limit=10
    )
    emergencies = await query_bus.ask(query)

    return emergencies.__dict__


@router.get("/emergencies/count")
@inject
async def count_emergencies(
    query_bus: QueryBus = Depends(Provide[Container.query_bus]),
):
    query = FindEmergenciesCounterQuery()
    count = await query_bus.ask(query)
    return count.__dict__


@router.get("/emergencies/count_per_user/{user_id}")
@inject
async def count_emergencies_per_user(
    user_id: str,
    query_bus: QueryBus = Depends(Provide[Container.query_bus]),
):
    query = FindEmergenciesCounterPerUserQuery(user_id=user_id)
    count = await query_bus.ask(query)
    return count.__dict__


@router.get("/emergencies/{emergency_id}")
@inject
async def find_emergency(
    emergency_id: str, query_bus: QueryBus = Depends(Provide[Container.query_bus])
):
    query = FindEmergencyQuery(emergency_id)
    emergency = await query_bus.ask(query)

    if emergency:
        return emergency.__dict__
    return {}
