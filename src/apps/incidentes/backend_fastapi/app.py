from fastapi import FastAPI

from apps.incidentes.__dependency_injection import Container
from apps.incidentes.backend_fastapi import views


def create_app() -> FastAPI:
    container = Container()

    app = FastAPI()
    app.container = container  # type: ignore[attr-defined]

    app.include_router(views.router)
    return app
