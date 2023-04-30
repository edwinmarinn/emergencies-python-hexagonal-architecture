from aio_pika.abc import AbstractIncomingMessage

from .rabbit_mq_connection_async import RabbitMqConnectionAsync
from ...domain_event_json_deserializer import DomainEventJsonDeserializer


class RabbitMqDomainEventsConsumerAsync:
    def __init__(
        self,
        connection: RabbitMqConnectionAsync,
        deserializer: DomainEventJsonDeserializer,
        exchange_name: str,
        max_retries: int,
    ):
        self._connection = connection
        self._deserializer = deserializer
        self._exchange_name = exchange_name
        self._max_retries = max_retries

    async def consume(self, subscriber, queue_name: str) -> None:
        try:
            queue = await self._connection.queue(queue_name)
            await queue.consume(self.consumer(subscriber))
        except Exception:  # Fixme: Change for a more specific exception
            # We don't want to raise an error if there are no messages in the queue
            pass

    def consumer(self, subscriber):
        async def _consumer(message: AbstractIncomingMessage):
            event = self._deserializer.deserialize(message.body)

            try:
                subscriber(event)
            except Exception as error:
                # self.handle_consumption_error(message)
                raise error

            await message.ack()

        return _consumer


#     private function handleConsumptionError(AMQPEnvelope $envelope, AMQPQueue $queue): void
#     {
#         $this->hasBeenRedeliveredTooMuch($envelope)
#             ? $this->sendToDeadLetter($envelope, $queue)
#             : $this->sendToRetry($envelope, $queue);
#
#         $queue->ack($envelope->getDeliveryTag());
#     }
#
#     private function hasBeenRedeliveredTooMuch(AMQPEnvelope $envelope): bool
#     {
#         return get('redelivery_count', $envelope->getHeaders(), 0) >= $this->maxRetries;
#     }
#
#     private function sendToDeadLetter(AMQPEnvelope $envelope, AMQPQueue $queue): void
#     {
#         $this->sendMessageTo(RabbitMqExchangeNameFormatter::deadLetter($this->exchangeName), $envelope, $queue);
#     }
#
#     private function sendToRetry(AMQPEnvelope $envelope, AMQPQueue $queue): void
#     {
#         $this->sendMessageTo(RabbitMqExchangeNameFormatter::retry($this->exchangeName), $envelope, $queue);
#     }
#
#     private function sendMessageTo(string $exchangeName, AMQPEnvelope $envelope, AMQPQueue $queue): void
#     {
#         $headers = $envelope->getHeaders();
#
#         $this->connection->exchange($exchangeName)->publish(
#             $envelope->getBody(),
#             $queue->getName(),
#             AMQP_NOPARAM,
#             [
#                 'message_id'       => $envelope->getMessageId(),
#                 'content_type'     => $envelope->getContentType(),
#                 'content_encoding' => $envelope->getContentEncoding(),
#                 'priority'         => $envelope->getPriority(),
#                 'headers'          => assoc($headers, 'redelivery_count', get('redelivery_count', $headers, 0) + 1),
#             ]
#         );
#     }
# }
