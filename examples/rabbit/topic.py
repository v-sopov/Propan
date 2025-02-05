from propan import PropanApp, RabbitBroker
from propan.annotations import Logger
from propan.brokers.rabbit import ExchangeType, RabbitExchange, RabbitQueue

broker = RabbitBroker()
app = PropanApp(broker)

topic_exchange = RabbitExchange("exchange", auto_delete=True, type=ExchangeType.TOPIC)
queue_1 = RabbitQueue("test-queue-1", auto_delete=True, routing_key="*.info")
queue_2 = RabbitQueue("test-queue-2", auto_delete=True, routing_key="*.debug")


@broker.handle(queue_1, topic_exchange)
async def base_handler1(logger: Logger):
    logger.info("base_handler1")


@broker.handle(queue_1, topic_exchange)
async def base_handler2(logger: Logger):
    logger.info("base_handler2")


@broker.handle(queue_2, topic_exchange)
async def base_handler3(logger: Logger):
    logger.info("base_handler3")


@app.on_startup
async def send_messages():
    await broker.start()

    await broker.publish(routing_key="logs.info", exchange=topic_exchange)
    await broker.publish(routing_key="logs.info", exchange=topic_exchange)
    await broker.publish(routing_key="logs.info", exchange=topic_exchange)
    await broker.publish(routing_key="logs.debug", exchange=topic_exchange)
