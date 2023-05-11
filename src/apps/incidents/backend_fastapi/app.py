from fastapi import FastAPI

from apps.incidents.__dependency_injection import Container, configure_event_bus
from apps.incidents.backend_fastapi import views


def create_app() -> FastAPI:
    container = Container()

    app = FastAPI(on_startup=[configure_event_bus(container)])
    app.container = container  # type: ignore[attr-defined]

    app.include_router(views.router)

    return app
