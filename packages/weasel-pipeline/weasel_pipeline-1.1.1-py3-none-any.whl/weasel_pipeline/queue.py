""" Contains functionality for working with RabbitMQ """
import asyncio
import pickle

import aio_pika
from aiormq.exceptions import ChannelInvalidStateError


class QueueHelper:
    """ Helper class for exchanging messages between elements of a weasel-pipeline toolchain """

    _queues = dict()
    _connection = None
    _channel = None

    @staticmethod
    async def create(amqp_uri: str, prefetch_count: int = 5000):
        """
        Create a QueueHelper instance and establish connection to the RabbitMQ server.

        :param amqp_uri: The connection URI for the RabbitMQ server
        :param prefetch_count:
            Controls the number of messages which are pre-fetched from each queue.
            Keeping this number high enough will significantly improve message throughput
        :return: The created QueueHelper instance
        """
        queue_helper = QueueHelper()
        await queue_helper.initialize_pika(amqp_uri, prefetch_count)
        return queue_helper

    async def initialize_pika(self, amqp_uri: str, prefetch_count: int) -> None:
        """
        Initialize the connection to RabbitMQ.
        This is only required if the instance is not created via the `create` method.

        :param amqp_uri: The connection URI for the RabbitMQ server
        :param prefetch_count:
            Controls the number of messages which are pre-fetched from each queue.
            Keeping this number high enough will significantly improve message throughput
        """
        self._connection = await aio_pika.connect_robust(
            amqp_uri, loop=asyncio.get_event_loop()
        )
        self._channel = await self._connection.channel()
        await self._channel.set_qos(prefetch_count=prefetch_count)

    async def close(self) -> None:
        """
        Close the connection to RabbitMQ.
        """
        await self._channel.close()
        await self._connection.close()

    async def declare_queue(self, name: str, queue_max_length: int = 1000) -> None:
        """
        Declare a queue with the given name.

        :param name: The identifying name for the created queue
        :param queue_max_length:
            Defines the maximum length of this queue. This prevents the queue from growing
            indefinitely. When an element calls `put_value` to a queue which is currently full,
            this call will be suspended until there is free space in the queue. This way all
            elements in the queue get restricted to the speed of the bottleneck elements.
        """
        queue = await self._channel.declare_queue(
            name,
            arguments={
                "x-max-length": queue_max_length,
                "x-overflow": "reject-publish",
            },
        )
        self._queues[name] = queue

    async def put_value(self, name: str, value: object) -> None:
        """
        Output a value to the queue of the given name. If the queue is currently full, this
        call will be suspended until there is free space again.

        :param name: The identifying name of the queue to which the value is written
        :param value: The output value. Can be any data type supported by `pickle`
        """
        while True:
            try:
                await self._channel.default_exchange.publish(
                    aio_pika.Message(body=pickle.dumps(value)), routing_key=name
                )
                return
            except (
                aio_pika.exceptions.DeliveryError,
                ChannelInvalidStateError,
                ConnectionResetError,
                ConnectionRefusedError,
                RuntimeError,
            ):
                await asyncio.sleep(0.1)

    async def pull_values(self, name: str):
        """
        Pull values from the queue of the given name. This will return an iterator that is
        supposed to be used in an `async for` loop.

        :param name: The identifying name of the queue from which the values are read
        """
        async for message in self._queues[name]:
            async with message.process():
                yield pickle.loads(message.body)
