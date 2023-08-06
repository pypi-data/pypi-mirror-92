from functools import cached_property
from typing import Optional, Callable, Any
from coresvc.serializer import serializer
from aio_pika import connect_robust, Connection, Channel, Message, Exchange, ExchangeType, IncomingMessage
from coresvc.base.base_service import BaseService


class AMQPClient(BaseService):
    def __init__(self, amqp_url, **kwargs):
        self.amqp_url = amqp_url
        super().__init__(**kwargs)

    def on_init_dependencies(self):
        return [self.producer, self.consumer]

    async def publish(self, topic: str, msg: dict):
        await self.producer.publish(topic, msg)

    async def subscribe(self, topic: str, handler: Callable):
        await self.consumer.subscribe(topic, handler)

    @cached_property
    def producer(self):
        return Producer(self.amqp_url, loop=self.loop, beacon=self.beacon)

    @cached_property
    def consumer(self):
        return Consumer(self.amqp_url, loop=self.loop, beacon=self.beacon)


class Producer(BaseService):
    def __init__(self, url, **kwargs):
        self.url = url
        self._connection: Optional[Connection] = None
        self._channel: Optional[Channel] = None
        self._exchange: Optional[Exchange] = None
        super().__init__(**kwargs)

    async def on_start(self) -> None:
        await self._wait_for_connection()
        self._channel = await self._connection.channel()
        self._exchange = await self._channel.declare_exchange('pubsub', type=ExchangeType.TOPIC)
        # TODO: Consider if exchange name should be
        #  - a single name for all or
        #  - multiple ones consistent with service namespace
        #  - this also depends on if we need more than one type of exchanges: fanout, direct, topic, etc

    async def on_started(self) -> None:
        self.log.info(self.label + 'started')

    async def on_stop(self) -> None:
        if self._connection:
            await self._connection.close()

    async def publish(self, topic: str, msg: dict):
        if not self.started:
            raise RuntimeError('service not started')
        message = Message(body=serializer.dumps(msg))
        await self._exchange.publish(message, routing_key=topic)

    async def _wait_for_connection(self, retry=0):
        try:
            self._connection = await connect_robust(self.url, loop=self.loop)
        except ConnectionError:
            if retry < 5:
                await self.sleep(3)
                return await self._wait_for_connection(retry+1)
            raise


class Consumer(BaseService):
    def __init__(self, url, **kwargs):
        self.url = url
        self._connection: Optional[Connection] = None
        self._channel: Optional[Channel] = None
        self._exchange: Optional[Exchange] = None
        self._msg_handlers = {}
        super().__init__(**kwargs)

    async def on_start(self) -> None:
        await self._wait_for_connection()
        self._channel = await self._connection.channel()
        self._exchange = await self._channel.declare_exchange('pubsub', type=ExchangeType.TOPIC)

        # Maximum message count which will be
        # processing at the same time.
        # await self._channel.set_qos(prefetch_count=100)

    async def on_started(self) -> None:
        self.log.info(self.label + 'started')

    async def on_stop(self) -> None:
        if self._connection:
            await self._connection.close()

    async def subscribe(self, topic: str, handler: Callable[[dict], Any]):
        if not self.started:
            raise RuntimeError('service not started')

        async def handler_wrapper(message: IncomingMessage):
            obj = serializer.loads(message.body)
            try:
                await handler(obj)
                message.ack()  # msg handled properly and positive acknowledge
            except Exception as e:
                self.log.exception(str(e))
                message.nack()  # msg wasn't handled properly, negative acknowledge and requeue.

        queue = await self._channel.declare_queue()
        await queue.bind(self._exchange, routing_key=topic)
        await queue.consume(handler_wrapper)

    async def _wait_for_connection(self, retry=0):
        try:
            self._connection = await connect_robust(self.url, loop=self.loop)
        except ConnectionError:
            if retry < 5:
                await self.sleep(3)
                return await self._wait_for_connection(retry+1)
            raise
