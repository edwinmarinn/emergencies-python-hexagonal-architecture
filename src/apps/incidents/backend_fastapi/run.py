import uvicorn

from apps.incidents.backend_fastapi.app import create_app


def main():
    import_string = f"{create_app.__module__}:{create_app.__name__}"

    uvicorn.run(app=import_string, host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
