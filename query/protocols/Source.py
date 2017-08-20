from ..connection import BaseUDP
from ..errors import ParsingError
from ..helpers import async_raise_on_timeout
from ..parser.helpers import QueryBytes


class SourceAbstract(BaseUDP):
    A2S_HEADER_MULTIPART = -2
    A2S_HEADER = -1

    A2S_REQUEST_CHALLENGE = -1
    A2S_RESPONSE_CHALLENGE = ord('A')

    A2S_INFO = ord('T')
    A2S_RESPONSE_INFO = ord('I')
    A2S_RESPONSE_INFO_OLD = ord('m')

    A2S_PLAYER = ord('U')
    A2S_RESPONSE_PLAYER = ord('D')

    A2S_RULES = ord('V')
    A2S_RESPONSE_RULES = ord('E')

    @async_raise_on_timeout
    async def get_info(self):
        reader, writer = await self._connection.connect()

        query = QueryBytes()
        query.append(self.A2S_HEADER, QueryBytes.LITTLE_TYPE_INT)
        query.append(self.A2S_INFO, QueryBytes.LITTLE_TYPE_CHAR)
        query.append('Source Engine Query', QueryBytes.TYPE_STRING)

        writer.write(query.buffer)
        return self.parse_info(QueryBytes(await reader.readline()))

    @async_raise_on_timeout
    async def get_players(self):
        reader, writer = await self._connection.connect()

        query = QueryBytes()
        query.append(self.A2S_HEADER, QueryBytes.LITTLE_TYPE_INT)
        query.append(self.A2S_PLAYER, QueryBytes.LITTLE_TYPE_CHAR)
        offset = len(query.buffer)
        query.append(self.A2S_REQUEST_CHALLENGE, QueryBytes.LITTLE_TYPE_INT)

        writer.write(query.buffer)

        challenge_code = self.parse_challenge(QueryBytes(await reader.readline()))
        query.replace(challenge_code, QueryBytes.LITTLE_TYPE_INT, offset=offset)

        writer.write(query.buffer)
        return self.parse_players(QueryBytes(await reader.readline()))

    @async_raise_on_timeout
    async def get_rules(self):
        reader, writer = await self._connection.connect()

        query = QueryBytes()
        query.append(self.A2S_HEADER, QueryBytes.LITTLE_TYPE_INT)
        query.append(self.A2S_RULES, QueryBytes.LITTLE_TYPE_CHAR)
        offset = len(query.buffer)
        query.append(self.A2S_REQUEST_CHALLENGE, QueryBytes.LITTLE_TYPE_INT)

        writer.write(query.buffer)

        challenge_code = self.parse_challenge(QueryBytes(await reader.readline()))
        query.replace(challenge_code, QueryBytes.LITTLE_TYPE_INT, offset=offset)

        writer.write(query.buffer)
        return self.parse_rules(QueryBytes(await self.read_multi_packet(reader)))

    async def read_multi_packet(self, reader):
        loop = 0
        list_data = []
        while True:
            loop += 1
            next_package = QueryBytes(await reader.readline())
            data = self.parse_multi_packet(next_package)
            list_data.append((data, next_package))

            if data['id'] != list_data[0][0]['id']:
                return None

            if loop >= data['total']:
                break

        return b''.join([p.buffer for d, p in sorted(list_data, key=lambda x: x[0]['number'])])

    def parse_multi_packet(self, response):
        raise NotImplementedError()

    def parse_info(self, response):
        raise NotImplementedError()

    def parse_rules(self, response):
        if response.pop(QueryBytes.LITTLE_TYPE_INT) != self.A2S_HEADER:
            raise ParsingError('Invalid header')

        if response.pop(QueryBytes.LITTLE_TYPE_CHAR) != self.A2S_RESPONSE_RULES:
            raise ParsingError('Invalid header')

        rules_num = response.pop(QueryBytes.LITTLE_TYPE_SHORT)
        list_rules = dict()
        for i in range(0, rules_num):
            name = response.pop(QueryBytes.TYPE_STRING)
            value = response.pop(QueryBytes.TYPE_STRING)
            list_rules.setdefault(name, list()).append(value)

        return list_rules

    def parse_players(self, response):
        if response.pop(QueryBytes.LITTLE_TYPE_INT) != self.A2S_HEADER:
            raise ParsingError('Invalid header')

        if response.pop(QueryBytes.LITTLE_TYPE_CHAR) != self.A2S_RESPONSE_PLAYER:
            raise ParsingError('Invalid header')

        players_num = response.pop(QueryBytes.LITTLE_TYPE_CHAR)
        list_players = list()
        for i in range(0, players_num):
            response.pop(QueryBytes.LITTLE_TYPE_CHAR)  # index
            name = response.pop(QueryBytes.TYPE_STRING)
            score = response.pop(QueryBytes.LITTLE_TYPE_LONG)
            duration = response.pop(QueryBytes.LITTLE_TYPE_FLOAT)
            list_players.append({
                'name': name,
                'score': score,
                'duration': duration,
            })
        return list_players

    def parse_challenge(self, response):
        if response.pop(QueryBytes.LITTLE_TYPE_INT) == self.A2S_HEADER:
            if response.pop(QueryBytes.LITTLE_TYPE_CHAR) == self.A2S_RESPONSE_CHALLENGE:
                return response.pop(QueryBytes.LITTLE_TYPE_INT)
        raise ParsingError('MALFORMED')


class Source(SourceAbstract):
    def parse_multi_packet(self, response):
        if response.get(QueryBytes.LITTLE_TYPE_INT, change_cursor=False) == self.A2S_HEADER:
            return {
                'id': '1',
                'total': 1,
                'number': 0,
            }

        if response.pop(QueryBytes.LITTLE_TYPE_INT) != self.A2S_HEADER_MULTIPART:
            raise ParsingError('Invalid header')

        id = response.pop(QueryBytes.LITTLE_TYPE_LONG)
        total = response.pop(QueryBytes.LITTLE_TYPE_CHAR)
        number = response.pop(QueryBytes.LITTLE_TYPE_CHAR)
        size = response.pop(QueryBytes.LITTLE_TYPE_SHORT)

        is_compressed = bool(id & 0x80000000)
        if is_compressed:
            raise NotImplementedError('add issue on github.')

        return {
            'id': id,
            'total': total,
            'number': number,
        }

    def parse_info(self, response):
        if response.pop(QueryBytes.LITTLE_TYPE_INT) != self.A2S_HEADER:
            raise ParsingError('Invalid header')

        header = response.pop(QueryBytes.LITTLE_TYPE_CHAR)
        if header != self.A2S_RESPONSE_INFO:
            raise ParsingError('Invalid header')

        response_data = dict()
        response_data['header'] = header

        response_data['protocol'] = response.pop(QueryBytes.LITTLE_TYPE_CHAR)
        response_data['hostname'] = response.pop(QueryBytes.TYPE_STRING)
        response_data['map'] = response.pop(QueryBytes.TYPE_STRING)
        response_data['folder'] = response.pop(QueryBytes.TYPE_STRING)
        response_data['game'] = response.pop(QueryBytes.TYPE_STRING)
        response_data['appid'] = response.pop(QueryBytes.LITTLE_TYPE_SHORT)
        response_data['players'] = response.pop(QueryBytes.LITTLE_TYPE_CHAR)
        response_data['maxplayers'] = response.pop(QueryBytes.LITTLE_TYPE_CHAR)
        response_data['bots'] = response.pop(QueryBytes.LITTLE_TYPE_CHAR)
        response_data['server_type'] = response.pop(QueryBytes.LITTLE_TYPE_CHAR)
        response_data['environment'] = response.pop(QueryBytes.LITTLE_TYPE_CHAR)
        response_data['password'] = response.pop(QueryBytes.LITTLE_TYPE_CHAR)
        response_data['vac'] = response.pop(QueryBytes.LITTLE_TYPE_CHAR)

        #the ship
        if response_data['appid'] == 2400:
            response_data['mode'] = response.pop(QueryBytes.LITTLE_TYPE_CHAR)
            response_data['witnesses'] = response.pop(QueryBytes.LITTLE_TYPE_CHAR)
            response_data['duration'] = response.pop(QueryBytes.LITTLE_TYPE_CHAR)

        response_data['version'] = response.pop(QueryBytes.TYPE_STRING)

        response_data['edf'] = response.pop(QueryBytes.LITTLE_TYPE_CHAR)
        if response_data['edf'] > 0:
            if response_data['edf'] & 0x80:
                response_data['gameport'] = response.pop(QueryBytes.LITTLE_TYPE_SHORT)

            if response_data['edf'] & 0x10:
                response_data['steamID'] = response.pop(QueryBytes.LITTLE_TYPE_LONGLONG)

            if response_data['edf'] & 0x40:
                response_data['tv_port'] = response.pop(QueryBytes.LITTLE_TYPE_SHORT)
                response_data['tv_name'] = response.pop(QueryBytes.TYPE_STRING)

            if response_data['edf'] & 0x20:
                response_data['tags'] = response.pop(QueryBytes.TYPE_STRING)

            if response_data['edf'] & 0x01:
                response_data['gameID'] = response.pop(QueryBytes.LITTLE_TYPE_LONGLONG)

                # fix for Just Cause 2, because he have in mapname our info for players and maxplayers
                # if response_data['gameID'] == 259080 and response_data['q_map'][0:9] == b'Players: ':
                #     parse_data = response_data['q_map'][9:].split(b'/')
                #
                #     response_data['q_maxplayers'] = self._any_to_bytes(parse_data[1])
                #     response_data['q_players'] = self._any_to_bytes(parse_data[0])
                #     response_data['q_map'] = b''

        return response_data


class GoldSource(SourceAbstract):
    def parse_multi_packet(self, response):
        if response.get(QueryBytes.LITTLE_TYPE_INT, change_cursor=False) == self.A2S_HEADER:
            return {
                'id': '1',
                'total': 1,
                'number': 0,
            }

        if response.pop(QueryBytes.LITTLE_TYPE_INT) != self.A2S_HEADER_MULTIPART:
            raise ParsingError('Invalid header')

        id = response.pop(QueryBytes.LITTLE_TYPE_LONG)
        packet_number = response.pop(QueryBytes.LITTLE_TYPE_CHAR)
        total = (packet_number >> 0) & 0xf
        number = (packet_number >> 4) & 0xf

        return {
            'id': id,
            'total': total,
            'number': number,
        }

    def parse_info(self, response):
        if response.pop(QueryBytes.LITTLE_TYPE_INT) != self.A2S_HEADER:
            raise ParsingError('Invalid header')

        header = response.pop(QueryBytes.LITTLE_TYPE_CHAR)
        if header != self.A2S_RESPONSE_INFO_OLD:
            raise ParsingError('Invalid header')

        response_data = dict()
        response_data['header'] = header

        response_data['address'] = response.pop(QueryBytes.TYPE_STRING)
        response_data['hostname'] = response.pop(QueryBytes.TYPE_STRING)
        response_data['map'] = response.pop(QueryBytes.TYPE_STRING)
        response_data['folder'] = response.pop(QueryBytes.TYPE_STRING)
        response_data['game'] = response.pop(QueryBytes.TYPE_STRING)
        response_data['players'] = response.pop(QueryBytes.LITTLE_TYPE_CHAR)
        response_data['maxplayers'] = response.pop(QueryBytes.LITTLE_TYPE_CHAR)
        response_data['protocol'] = response.pop(QueryBytes.LITTLE_TYPE_CHAR)
        response_data['server_type'] = response.pop(QueryBytes.LITTLE_TYPE_CHAR)
        response_data['environment'] = response.pop(QueryBytes.LITTLE_TYPE_CHAR)
        response_data['password'] = response.pop(QueryBytes.LITTLE_TYPE_CHAR)

        response_data['mod'] = response.pop(QueryBytes.LITTLE_TYPE_CHAR)
        if response_data['mod'] == 0x01:
            response_data['link'] = response.pop(QueryBytes.TYPE_STRING)
            response_data['download_link'] = response.pop(QueryBytes.TYPE_STRING)

            response.pop(QueryBytes.LITTLE_TYPE_BYTE)  # null byte

            response_data['version'] = response.pop(QueryBytes.LITTLE_TYPE_LONG)
            response_data['size'] = response.pop(QueryBytes.LITTLE_TYPE_LONG)
            response_data['type'] = response.pop(QueryBytes.LITTLE_TYPE_CHAR)
            response_data['dll'] = response.pop(QueryBytes.LITTLE_TYPE_CHAR)

        response_data['vac'] = response.pop(QueryBytes.LITTLE_TYPE_CHAR)
        response_data['bots'] = response.pop(QueryBytes.LITTLE_TYPE_CHAR)

        return response_data
