from abc import ABC
from collections import Counter
from typing import Optional, Type, Callable
from types import TracebackType

from propan.logger import empty


class BaseWatcher(ABC):
    max_tries: int

    def __init__(self, logger=empty, max_tries: int = None):
        self.logger = logger
        self.max_tries = max_tries

    def add(self, message_id: str) -> None:
        raise NotImplementedError()

    def is_max(self, message_id: str) -> bool:
        raise NotImplementedError()

    def remove(self, message_id: str):
        raise NotImplementedError()


class FakePushBackWatcher(BaseWatcher):
    def add(self, message_id: str):
        pass

    def is_max(self, message_id: str):
        return False

    def remove(self, message_id: str):
        pass


class PushBackWatcher(BaseWatcher):
    memory = Counter()

    def __init__(self, logger, max_tries: int = 3):
        super().__init__(logger, max_tries)

    def add(self, message_id: str) -> None:
        self.memory[message_id] += 1

    def is_max(self, message_id: str) -> bool:
        is_max = self.memory[message_id] > self.max_tries
        if is_max:
            self.logger.error(f'Already retried {self.max_tries} times. Skipped.')
        else:
            self.logger.error('Error is occured. Pushing back to queue.')
        return is_max

    def remove(self, message: str) -> None:
        self.memory[message] = 0
        self.memory += Counter()


class WatcherContext:
    def __init__(self,
                 watcher: BaseWatcher,
                 message_id,
                 *args,
                 on_success: Callable = lambda: None,
                 on_max: Callable = lambda: None,
                 on_error: Callable = lambda: None):
        self.watcher = watcher
        self.on_success = on_success
        self.on_max = on_max
        self.on_error = on_error
        self._message_id = message_id

    async def __aenter__(self):
        self.watcher.add(self._message_id)

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        if not exc_type:
            await self.on_success()
            self.watcher.remove(self._message_id)

        elif self.watcher.is_max(self._message_id):
            await self.on_max()
            self.watcher.remove(self._message_id)

        else:
            await self.on_error()
