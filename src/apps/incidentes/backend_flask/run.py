import uvicorn

from apps.incidentes.backend_flask.app import create_asgi_app


def main():
    import_string = f"{create_asgi_app.__module__}:{create_asgi_app.__name__}"

    uvicorn.run(app=import_string, host="0.0.0.0", port=5000, reload=True)


if __name__ == "__main__":
    main()
