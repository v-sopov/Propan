from propan import PropanApp, RabbitBroker
from propan.annotations import Logger
from propan.brokers.rabbit import RabbitExchange, RabbitQueue, ExchangeType

broker = RabbitBroker()
app = PropanApp(broker)

exch = RabbitExchange("exch", auto_delete=True, type=ExchangeType.FANOUT)

queue_1 = RabbitQueue("test-q-1", auto_delete=True)
queue_2 = RabbitQueue("test-q-2", auto_delete=True)

@broker.handle(queue_1, exch)
async def base_handler1(logger: Logger):
    logger.info("base_handler1")

@broker.handle(queue_1, exch)
async def base_handler2(logger: Logger):
    logger.info("base_handler2")

@broker.handle(queue_2, exch)
async def base_handler3(logger: Logger):
    logger.info("base_handler3")

@app.on_startup
async def send_messages():
    await broker.start()

    await broker.publish(exchange=exch)  # handlers: 1, 3
    await broker.publish(exchange=exch)  # handlers: 2, 3
    await broker.publish(exchange=exch)  # handlers: 1, 3
    await broker.publish(exchange=exch)  # handlers: 2, 3