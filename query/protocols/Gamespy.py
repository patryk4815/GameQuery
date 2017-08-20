from ..connection import BaseUDP
from ..helpers import async_raise_on_timeout
from ..parser.helpers import QueryBytes


class Gamespy1(BaseUDP):
    @async_raise_on_timeout
    async def get_info(self):
        reader, writer = await self._connection.connect()

        query = QueryBytes()
        query.append(b'\\info\\', None)

        writer.write(query.buffer)

        return self.parse_info(QueryBytes(await reader.readline()))

    def parse_info(self, response):
        list_info = list()

        list_split = response.buffer[1:].split(b'\\')
        list_info = list(zip(list_split[::2], list_split[1::2]))

        return list_info


class Gamespy2(BaseUDP):
    @async_raise_on_timeout
    async def get_info(self):
        reader, writer = await self._connection.connect()

        query = QueryBytes()
        query.append(b'\xFE\xFD\x00\x43\x4F\x52\x59\xFF\x00\x00', None)

        writer.write(query.buffer)

        return self.parse_info(QueryBytes(await reader.readline()))

    def parse_info(self, response):
        # if response[0:5] != b'\x00CORY':
        # list_commands = response[5:].split(b'\x00\x00\x00')[0].split(b'\x00')

        list_info = list()

        list_split = response.buffer[5:].split(b'\x00\x00\x00')[0].split(b'\x00')
        list_info = list(zip(list_split[::2], list_split[1::2]))

        return list_info


class Gamespy3(BaseUDP):
    is_challenge = False

    @async_raise_on_timeout
    async def get_info(self):
        reader, writer = await self._connection.connect()

        timestamp = b'\x04\x05\x06\x07'  # timestamp

        query = QueryBytes()
        query.append(b'\xFE\xFD\x09', None)
        query.append(timestamp, None)

        if self.is_challenge:
            writer.write(query.buffer)

            response = QueryBytes(await reader.readline())
            if response.buffer[:5] != b'\x09' + timestamp:
                raise Exception()  # fixme

            challange_int = int(response.buffer[5:-1]).to_bytes(4, 'big', signed=True)
            query.append(challange_int, None)

        query.append(b'\xFF\x00\x00\x01', None)
        query.set(b'\x00', QueryBytes.BIG_TYPE_BYTE, 1, offset=2)

        writer.write(query.buffer)
        return self.parse_info(QueryBytes(await reader.readline()))

    def parse_info(self, response):
        # if response[0] != 0x00 or response[1:5] != timestamp or response[15] != 0x00:
        # list_commands = response
        # list_commands.remove('p1073741829')  # fix for Unreal Tournament 3 because he have invalid data ?
        list_info = list()

        list_split = response.buffer[16:-2].split(b'\x00\x00\x01')[0].split(b'\x00')
        list_info = list(zip(list_split[::2], list_split[1::2]))

        return list_info


class Gamespy4(Gamespy3):
    is_challenge = True
