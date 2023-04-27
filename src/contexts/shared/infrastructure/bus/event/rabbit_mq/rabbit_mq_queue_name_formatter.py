from contexts.shared.domain.bus.event import DomainEventSubscriber
from contexts.shared.domain.utils.strings import camel_case_to_snake_case


class RabbitMqQueueNameFormatter:
    def __init__(self, company: str):
        self._company = company

    def format(self, subscriber: DomainEventSubscriber) -> str:
        subscriber_class_path = subscriber.__class__.__module__.split(".")

        queue_name_parts = [
            self._company,
            subscriber_class_path[1],
            subscriber_class_path[2],
            subscriber_class_path[-1],
        ]
        queue_name = ".".join(map(camel_case_to_snake_case, queue_name_parts))

        return queue_name

    def format_retry(self, subscriber: DomainEventSubscriber) -> str:
        queue_name = self.format(subscriber)

        return f"retry.{queue_name}"

    def format_dead_letter(self, subscriber: DomainEventSubscriber) -> str:
        queue_name = self.format(subscriber)

        return f"dead_letter.{queue_name}"

    @staticmethod
    def short_format(subscriber: DomainEventSubscriber) -> str:
        class_name = subscriber.__class__.__name__
        queue_name = camel_case_to_snake_case(class_name)
        return queue_name
