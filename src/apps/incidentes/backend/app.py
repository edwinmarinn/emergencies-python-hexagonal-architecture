from flask import Flask

from apps.incidentes.backend import views
from apps.incidentes.backend.dependency_injection import Container


def create_app() -> Flask:
    container = Container()

    app = Flask(__name__)
    app.container = container  # type: ignore[attr-defined]

    app.add_url_rule(
        "/emergencias/<emergencia_id>",
        "find_emergencia",
        views.find_emergencia,
        methods=["GET"],
    )
    app.add_url_rule(
        "/emergencias/", "create_emergencia", views.create_emergencia, methods=["PUT"]
    )
    app.add_url_rule(
        "/emergencias/", "list_emergencias", views.list_emergencia, methods=["GET"]
    )

    return app


if __name__ == "__main__":
    _app = create_app()
    _app.run(debug=True)
