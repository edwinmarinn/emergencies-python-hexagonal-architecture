from fastapi import FastAPI

from apps.incidents.__dependency_injection import Container, configure_event_bus
from apps.incidents.backend_fastapi import views


def create_app() -> FastAPI:
    container = Container()

    app = FastAPI(
        on_startup=[container.init_resources, configure_event_bus(container)],
        on_shutdown=[container.shutdown_resources],
    )
    app.container = container  # type: ignore[attr-defined]

    app.include_router(views.router)

    return app
