from contexts.shared.domain.utils.functions import retry_on_error

from .aws_container import AwsContainer


def configure_sns_sqs_event_bus(
    container: AwsContainer, retries: int = 5, interval: int = 5
):
    @retry_on_error(retries=retries, interval=interval, exception_class=Exception)
    async def configure_sqs():
        sqs_configurer = container.sqs_configurer()
        await sqs_configurer.configure(
            sns_topic_name=container.sns_topic_name(),
            subscribers=container.event_subscribers(),
        )

    @retry_on_error(retries=retries, interval=interval, exception_class=Exception)
    async def configure_subscribers():
        event_bus = container.event_bus()
        await event_bus.add_subscribers(container.event_subscribers())

    async def configure():
        await configure_sqs()
        await configure_subscribers()

    return configure
