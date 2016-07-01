import asyncio
from .udp import open_datagram_connection
from .tcp import open_connection
from .helpers import Timeout

__all__ = (
    'open_datagram_connection',
    'open_connection',
    'Timeout',
    'BaseUDP',
    'BaseTCP',
)


class Base(object):
    def __init__(self, *, ip, port, timeout, loop=None):
        if loop is None:
            loop = asyncio.get_event_loop()

        self._ip = ip
        self._port = port
        self._timeout = timeout
        self._loop = loop


class UDPConnector(Base):
    def __init__(self, *, ip, port, timeout, loop=None):
        super().__init__(ip=ip, port=port, timeout=timeout, loop=loop)
        self._is_closed = False
        self._conns = list()

    async def connect(self):
        args = await open_datagram_connection(
            self._ip,
            self._port,
            timeout_connection=self._timeout,
            loop=self._loop
        )
        self._conns.append(args)
        return args

    def close(self):
        if self._is_closed:
            return

        self._is_closed = True
        for reader, writer in self._conns:
            writer.close()


class BaseUDP(Base):
    def __init__(self, *, ip, port, timeout, loop=None):
        super().__init__(ip=ip, port=port, timeout=timeout, loop=loop)
        self._connection = UDPConnector(ip=ip, port=port, timeout=timeout, loop=loop)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self._connection.close()


class BaseTCP(Base):
    pass
