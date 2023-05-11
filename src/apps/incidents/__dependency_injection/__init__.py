import os
from typing import Any, Dict, TypedDict

from .aws import AwsContainer
from .local import LocalContainer, configure_rabbitmq_event_bus


class Option(TypedDict):
    container_class: Any
    configure_event_bus: Any


_containers: Dict[str, Option] = {
    "aws": {"container_class": AwsContainer, "configure_event_bus": None},
    "local": {
        "container_class": LocalContainer,
        "configure_event_bus": configure_rabbitmq_event_bus,
    },
}

_injector_container = os.environ["INJECTOR_CONTAINER"].strip()

Container = _containers[_injector_container]["container_class"]


def configure_event_bus(container):
    function = _containers[_injector_container].get("configure_event_bus")
    if function is not None:
        return function(container)
    return lambda: None
