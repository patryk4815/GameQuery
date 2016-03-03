import asyncio

__all__ = [
    'Timeout',
]


class Timeout:
    """
    This is copy from aiohttp helpers.py
    """
    def __init__(self, timeout, *, loop=None):
        self._timeout = timeout
        if loop is None:
            loop = asyncio.get_event_loop()
        self._loop = loop
        self._task = None
        self._cancelled = False
        self._cancel_handler = None

    def __enter__(self):
        self._task = asyncio.Task.current_task(loop=self._loop)
        if self._task is None:
            raise RuntimeError('Timeout context manager should be used '
                               'inside a task')
        self._cancel_handler = self._loop.call_later(
            self._timeout, self._cancel_task)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is asyncio.CancelledError and self._cancelled:
            self._cancel_handler = None
            self._task = None
            raise asyncio.TimeoutError
        self._cancel_handler.cancel()
        self._cancel_handler = None
        self._task = None

    def _cancel_task(self):
        self._cancelled = self._task.cancel()
