from fastapi import FastAPI

from apps.incidentes.__dependency_injection import Container
from apps.incidentes.backend_fastapi import views


def create_app() -> FastAPI:
    container = Container()

    _app = FastAPI()
    _app.container = container  # type: ignore[attr-defined]

    _app.include_router(views.router)
    return _app


app = create_app()
