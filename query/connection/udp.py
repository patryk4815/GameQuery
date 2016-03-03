import asyncio
import logging
from asyncio.futures import Future

__all__ = [
    'open_datagram_connection',
]
_DEFAULT_LIMIT = 2**16


class StreamReaderProtocol:
    def __init__(self, stream_reader, loop, timeout=None):
        self._timeout = timeout or 60

        self._loop = loop
        self._stream_reader = stream_reader
        self._transport = None

    def connection_made(self, transport):
        self._transport = transport
        self._stream_reader.set_transport(transport)
        self._loop.call_later(self._timeout, self.check_timeouts)

    def check_timeouts(self):
        current_time = self._loop.time()
        if 1 < current_time:
            self._transport.close()
            return
        self._loop.call_later(1, self.check_timeouts)

    def datagram_received(self, data, addr):
        logging.debug('datagram_received: {}'.format(data))
        self._stream_reader.feed_data(data)

    def error_received(self, exc):
        logging.critical('Error received:: {}'.format(exc))

    def connection_lost(self, exc):
        self._stream_reader.feed_eof()


class StreamWriter:
    def __init__(self, transport, protocol, reader, loop):
        self._transport = transport
        self._protocol = protocol
        assert reader is None or isinstance(reader, StreamReader)
        self._reader = reader
        self._loop = loop

    def write(self, data):
        logging.debug('write: {}'.format(data))
        self._transport.sendto(data)

    def close(self):
        return self._transport.close()


class StreamReader:
    def __init__(self, limit=_DEFAULT_LIMIT, loop=None):
        # The line length limit is  a security feature;
        # it also doubles as half the buffer limit.
        self._limit = limit
        if loop is None:
            self._loop = asyncio.get_event_loop()
        else:
            self._loop = loop

        self._buffer_sum = 0
        self._buffer_line = list()
        self._eof = False    # Whether we're done.
        self._waiter = None  # A future used by _wait_for_data()
        self._exception = None
        self._transport = None
        self._paused = False

    def exception(self):
        return self._exception

    def set_exception(self, exc):
        self._exception = exc

        waiter = self._waiter
        if waiter is not None:
            self._waiter = None
            if not waiter.cancelled():
                waiter.set_exception(exc)

    def _wakeup_waiter(self):
        """Wakeup read() or readline() function waiting for data or EOF."""
        waiter = self._waiter
        if waiter is not None:
            self._waiter = None
            if not waiter.cancelled():
                waiter.set_result(None)

    def set_transport(self, transport):
        assert self._transport is None, 'Transport already set'
        self._transport = transport

    def _maybe_resume_transport(self):
        if self._paused and self._buffer_sum <= self._limit:
            self._paused = False
            self._transport.resume_reading()

    def feed_eof(self):
        self._eof = True
        self._wakeup_waiter()

    def at_eof(self):
        """Return True if the buffer is empty and 'feed_eof' was called."""
        return self._eof and not self._buffer_sum

    def feed_data(self, data):
        assert not self._eof, 'feed_data after feed_eof'

        if not data:
            return

        self._buffer_line.append(data)
        self._buffer_sum += len(data)
        self._wakeup_waiter()

        if (self._transport is not None and
            not self._paused and
            self._buffer_sum > 2*self._limit):
            try:
                self._transport.pause_reading()
            except NotImplementedError:
                # The transport can't be paused.
                # We'll just have to buffer all data.
                # Forget the transport so we don't keep trying.
                self._transport = None
            else:
                self._paused = True

    async def _wait_for_data(self, func_name):
        """Wait until feed_data() or feed_eof() is called."""
        # StreamReader uses a future to link the protocol feed_data() method
        # to a read coroutine. Running two read coroutines at the same time
        # would have an unexpected behaviour. It would not possible to know
        # which coroutine would get the next data.
        if self._waiter is not None:
            raise RuntimeError('%s() called while another coroutine is '
                               'already waiting for incoming data' % func_name)

        self._waiter = Future(loop=self._loop)
        try:
            await self._waiter
        finally:
            self._waiter = None

    async def readline(self):
        if self._exception is not None:
            raise self._exception

        line = bytearray()
        not_enough = True

        while not_enough:
            while self._buffer_line and not_enough:
                line = self._buffer_line.pop(0)
                self._buffer_sum -= len(line)
                not_enough = False

                if len(line) > self._limit:
                    self._maybe_resume_transport()
                    raise ValueError('Line is too long')

            if self._eof:
                break

            if not_enough:
                await self._wait_for_data('readline')

        self._maybe_resume_transport()
        return bytes(line)

    async def read(self, n=-1):
        if self._exception is not None:
            raise self._exception

        if not n:
            return b''

        if n < 0:
            # This used to just loop creating a new waiter hoping to
            # collect everything in self._buffer, but that would
            # deadlock if the subprocess sends more than self.limit
            # bytes.  So just call self.read(self._limit) until EOF.
            blocks = []
            while True:
                block = await self.read(self._limit)
                if not block:
                    break
                blocks.append(block)
            return b''.join(blocks)
        else:
            if not self._buffer_line and not self._eof:
                await self._wait_for_data('read')

        join_data = bytes(b''.join(self._buffer_line))
        if n < 0 or self._buffer_sum <= n:
            data = join_data
            self._buffer_line = list()
            self._buffer_sum = 0
        else:
            # n > 0 and len(self._buffer) > n
            data = bytes(join_data[:n])
            self._buffer_line = [join_data[n:]]
            self._buffer_sum = len(self._buffer_line[0])
            logging.critical(self._buffer_line)

        self._maybe_resume_transport()
        return data

    async def __aiter__(self):
        return self

    async def __anext__(self):
        val = await self.readline()
        if val == b'':
            raise StopAsyncIteration
        return val


async def open_datagram_connection(host=None, port=None, loop=None, timeout_connection=None, limit=_DEFAULT_LIMIT, **kwds):
    if loop is None:
        loop = asyncio.get_event_loop()

    reader = StreamReader(limit=limit, loop=loop)
    protocol = StreamReaderProtocol(reader, loop=loop, timeout=timeout_connection)
    transport, _ = await loop.create_datagram_endpoint(
        lambda: protocol, remote_addr=(host, port), **kwds
    )
    writer = StreamWriter(transport, protocol, reader, loop)
    return reader, writer
