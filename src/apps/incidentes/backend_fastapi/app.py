from fastapi import FastAPI

from apps.incidentes.__dependency_injection import Container
from apps.incidentes.__dependency_injection.configure_event_bus import (
    configure_event_bus,
)
from apps.incidentes.backend_fastapi import views


def create_app() -> FastAPI:
    container = Container()

    app = FastAPI(on_startup=[configure_event_bus(container)])
    app.container = container  # type: ignore[attr-defined]

    app.include_router(views.router)

    return app
