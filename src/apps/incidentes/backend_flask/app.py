from flask import Flask
from asgiref.wsgi import WsgiToAsgi

from apps.incidentes.__dependency_injection import Container
from apps.incidentes.backend_flask import views


# The problem with Flask async views and async globals
# https://sethmlarson.dev/flask-async-views-and-async-globals

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


app = WsgiToAsgi(create_app())
