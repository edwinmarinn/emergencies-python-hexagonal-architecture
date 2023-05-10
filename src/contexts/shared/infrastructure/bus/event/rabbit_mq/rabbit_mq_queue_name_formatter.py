from contexts.shared.infrastructure.bus.event import QueueNameFormatter


class RabbitMqQueueNameFormatter(QueueNameFormatter):
    def __init__(self, company: str):
        super().__init__(company=company, separator=".", use_long_format=True)
