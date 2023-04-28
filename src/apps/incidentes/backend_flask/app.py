from flask import Flask

from apps.incidentes.__dependency_injection import Container
from apps.incidentes.backend_flask import views


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
    _app.run(host="0.0.0.0", port=5000, debug=True)
