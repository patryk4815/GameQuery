from ..connection import BaseUDP
from ..helpers import async_raise_on_timeout
from ..parser.helpers import QueryBytes


class Quake3(BaseUDP):
    @async_raise_on_timeout
    async def get_info(self):
        reader, writer = await self._connection.connect()

        query = QueryBytes()
        query.append(b'\xFF\xFF\xFF\xFFgetstatus\x0A', None)

        writer.write(query.buffer)

        return self.parse_info(QueryBytes(await reader.readline()))

    def parse_info(self, response):
        #  b'\xff\xff\xff\xffstatusResponse\n\\type\\-

        list_info = list()

        list_split = response.buffer[20:].split(b'\\')
        list_info = list(zip(list_split[::2], list_split[1::2]))

        return list_info
