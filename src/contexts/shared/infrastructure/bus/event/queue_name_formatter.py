from contexts.shared.domain.bus.event import DomainEventSubscriber
from contexts.shared.domain.utils.strings import camel_case_to_snake_case


class QueueNameFormatter:
    def __init__(self, company: str, separator: str = ".", use_long_format=True):
        self._company = company
        self._separator = separator
        self.format = self._long_format if use_long_format else self._short_format

    def _long_format(self, subscriber: DomainEventSubscriber) -> str:
        subscriber_class_path = subscriber.__class__.__module__.split(".")

        queue_name_parts = [
            self._company,
            subscriber_class_path[1],
            subscriber_class_path[2],
            subscriber_class_path[-1],
        ]
        queue_name = self._separator.join(
            map(camel_case_to_snake_case, queue_name_parts)
        )

        return queue_name

    @staticmethod
    def _short_format(subscriber: DomainEventSubscriber) -> str:
        class_name = subscriber.__class__.__name__
        queue_name = camel_case_to_snake_case(class_name)
        return queue_name

    def format_retry(self, subscriber: DomainEventSubscriber) -> str:
        queue_name = self.format(subscriber)

        return f"retry{self._separator}{queue_name}"

    def format_dead_letter(self, subscriber: DomainEventSubscriber) -> str:
        queue_name = self.format(subscriber)

        return f"dead_letter{self._separator}{queue_name}"
