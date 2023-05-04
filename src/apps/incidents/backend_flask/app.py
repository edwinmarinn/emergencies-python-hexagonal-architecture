from asgiref.wsgi import WsgiToAsgi
from flask import Flask

from apps.incidents.__dependency_injection import Container
from apps.incidents.backend_flask import views


def create_app() -> Flask:
    container = Container()

    app = Flask(__name__)
    app.container = container  # type: ignore[attr-defined]

    app.add_url_rule(
        "/emergencies/<emergency_id>",
        "find_emergency",
        views.find_emergency,
        methods=["GET"],
    )
    app.add_url_rule(
        "/emergencies/", "create_emergency", views.create_emergency, methods=["PUT"]
    )
    app.add_url_rule(
        "/emergencies/", "list_emergencies", views.list_emergency, methods=["GET"]
    )
    return app


def create_asgi_app():
    # The problem with Flask async views and async globals
    # https://sethmlarson.dev/flask-async-views-and-async-globals

    app = WsgiToAsgi(create_app())
    return app
