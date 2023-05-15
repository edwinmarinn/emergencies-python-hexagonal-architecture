import uvicorn
from environs import Env


def load_environment_variables():
    env = Env()
    env.read_env(
        path="/home/ssd/programming/emergencias-python-arquitectura-hexagonal/.env.default",
        override=True,
    )
    env.read_env(
        path="/home/ssd/programming/emergencias-python-arquitectura-hexagonal/.env.local",
        override=True,
    )


def main():
    load_environment_variables()

    from apps.incidents.backend_fastapi.app import create_app

    import_string = f"{create_app.__module__}:{create_app.__name__}"
    uvicorn.run(app=import_string, host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
