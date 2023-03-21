import asyncio
from typing import Optional, Callable, List, Dict, Any, NoReturn
from pathlib import Path
import inspect

from propan.logger import empty
from propan.logger.model.usecase import LoggerUsecase

from propan.config import init_settings

from propan.brokers.model.bus_usecase import BrokerUsecase
from propan.utils.context.decorate import global_context


class PropanApp:
    _instanse = None
    _context: Dict[str, Any] = {}
    _on_startup_calling: List[Callable] = []
    _on_shutdown_calling: List[Callable] = []

    def __new__(cls, *args, **kwargs):
        if cls._instanse is None:
            cls._instanse = super().__new__(cls)
        return cls._instanse

    def __init__(
        self,
        broker: Optional[BrokerUsecase] = None,
        logger: LoggerUsecase = empty,
        settings_dir: Optional[Path] = None,
        *args, **kwargs
    ):
        if settings_dir:
            self.settings = init_settings(settings_dir, settings_dir="")

        self.broker = broker
        self.logger = logger

        self.loop = asyncio.get_event_loop()

        self._context = global_context
        self.set_context("app", self)
        self.set_context("broker", self.broker)
        self.set_context("logger", self.logger)


    async def startup(self):
        if (broker := self.broker) is not None:
            self.logger.info(f"Listening: {', '.join((i.queue.name for i in broker.handlers))} queues")
            await broker.start()

        for func in self._on_startup_calling:
            f = func()
            if inspect.isawaitable(f):
                await f

    async def shutdown(self):
        if getattr(self.broker, "_connection", False) is not False:
            await self.broker.close()

        for func in self._on_shutdown_calling:
            f = func()
            if inspect.isawaitable(f):
                await f

    def run(self) -> NoReturn:
        try:
            self.logger.info("Propan app starting...")
            self.loop.run_until_complete(self.startup())
            self.logger.info("Propan app started successfully! To exit press CTRL+C")
            self.loop.run_forever()
        finally:
            self.logger.info("Propan app shutting down...")
            self.loop.run_until_complete(self.shutdown())
            self.logger.info("Propan app shut down gracefully.")

    def on_startup(self, func: Callable):
        self._on_startup_calling.append(func)
        return func

    def on_shutdown(self, func: Callable):
        self._on_shutdown_calling.append(func)
        return func

    def set_context(self, key: str, v: Any):
        self._context[key] = v
